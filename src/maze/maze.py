import random
from arcade import Vec2, Rect

from src.visual.vatlas import VAtlas
from src.utils.usage import sprite_center
from src.visual.sprites.swall import SWall
from src.visual.pathfinding.bfs import BFS
from src.visual.sprites.sfloor import SFloor
from src.visual.vdata import VData, DebugMode
from src.visual.sprites.sfloor_debug import SFloorDebug


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class Maze:
    """
    Maze class
    From a raw maze list[list[int]] where:
        - 0 -> floor
        - 1 -> wall

    Build and manage SWall and SFloor.
    Use sprite_lists properties for the maze such as center_position or rect...
    """

    NEIGHBOURS: list[Vec2] = [
        Vec2(-VData.SPRITE_SIZE, VData.SPRITE_SIZE),
        Vec2(0, VData.SPRITE_SIZE),
        Vec2(VData.SPRITE_SIZE, VData.SPRITE_SIZE),
        Vec2(VData.SPRITE_SIZE, 0),
        Vec2(VData.SPRITE_SIZE, -VData.SPRITE_SIZE),
        Vec2(0, -VData.SPRITE_SIZE),
        Vec2(-VData.SPRITE_SIZE, -VData.SPRITE_SIZE),
        Vec2(-VData.SPRITE_SIZE, 0),
    ]

    def __init__(
        self,
        atlas: VAtlas,
        raw_maze: list[list[int]],
        floor_as_frame: bool = False,
    ) -> None:
        self.raw_maze = raw_maze
        self.atlas = atlas

        # Sprites --
        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas, frame_texture=floor_as_frame)
        self.floors_debug: SFloorDebug = SFloorDebug(self.atlas)

        # Graph --
        self.graph_neighbours: dict[Vec2, list[Vec2]] = dict()
        self.graph_costs: dict[Vec2, int] = dict()
        self.graph_corners: list[dict[Vec2, int]] = list()

    # ########################################################################
    # ############################################################# BUILD ####
    def build(
        self,
        sprite_offset: Vec2 = Vec2(0, 0),
        include_graph: bool = False,
    ) -> None:
        """
        Build the maze, its sprites and the graph for the BFS.
        include_graph = False to skip the algorithm management.
        """

        self._build_sprites(sprite_offset)

        if include_graph:
            self._build_floor_graph()
            self.bfs = BFS(self.graph_neighbours)

            self.graph_corners = list()
            for corner in self.floor_corners:
                self.graph_corners.append(self.bfs.get_costs(corner))

    # ########################################################################
    # ##################################################### BUILD SPRITES ####
    def _build_sprites(self, offset: Vec2 = Vec2(0, 0)) -> None:
        wall_points: set[Vec2] = set()
        floor_points: set[Vec2] = set()

        # !! Reverse the rows to switch in X/Y !!
        sprite_size = VData.SPRITE_SIZE
        for y, row in enumerate(reversed(self.raw_maze)):
            for x, value in enumerate(row):
                point = Vec2(
                    x * sprite_size + offset.x,
                    y * sprite_size + offset.y,
                )

                if value == 1:
                    wall_points.add(point)
                else:
                    floor_points.add(point)

        self.walls.reload(wall_points, floor_points)
        self.floors.reload(floor_points)
        self.floors_debug.reload_maze(floor_points)

    # ########################################################################
    # ################################################# BUILD FLOOR GRAPH ####
    def _build_floor_graph(self) -> None:
        """
        From the floor sprites,
        build a dict which will be used by the BFS algorithm.
        Each entry is a point (sprite center) with its list of neighbours.
        """

        self.graph_neighbours = {
            sprite_center(sp): [] for sp in self.floors.sprites
        }

        for point, neighbours in self.graph_neighbours.items():
            for possible_neighbour in (n + point for n in Maze.NEIGHBOURS):
                if possible_neighbour in self.graph_neighbours.keys():
                    neighbours.append(possible_neighbour)

    # ########################################################################
    # ############################################### UPDATE GRAPH VALUES ####
    def update_graph_values(self, start: Vec2) -> None:
        """
        Relaunch the algorithm from the player on the entire maze.
        """
        self.graph_costs = self.bfs.get_costs(start)
        self.floors_debug.update_costs(self.graph_costs)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.walls.draw()
        self.floors.draw()
        if VData.debug_mode == DebugMode.ALGO:
            self.floors_debug.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.walls.update(delta_time)
        self.floors.update(delta_time)

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self) -> Vec2:
        return self.walls.center_position

    @property
    def rect(self) -> Rect:
        return self.walls.rect

    @property
    def height(self) -> int:
        return self.walls.height

    @property
    def width(self) -> int:
        return self.walls.width

    @property
    def floor_center(self) -> Vec2:
        return self.floors.sprite_center

    @property
    def floor_corners(self) -> list[Vec2]:
        return self.floors.sprite_corners

    # ########################################################################
    # ################################################### CLOSET FLOOR OF ####
    def closest_floor_of(self, point: Vec2) -> Vec2:
        """Helper of 'find closest sprite' for floor"""

        return self.floors.find_closest_sprite_of(point)

    # ########################################################################
    # ################################################### GET NEXT LOWEST ####
    # TODO: To refactor
    # TODO: To refactor
    def get_next_lowest(
        self,
        point: Vec2,
        reversed: bool = False,
        corner: int | None = None,
    ) -> Vec2:
        """Get the point neighbour with the lowest cost."""

        def next_one(graph_costs: dict, point: Vec2, reversed: bool) -> Vec2:

            if graph_costs and graph_costs[point] > 0:
                neighbours = self.graph_neighbours[point]
                with_costs = {n: graph_costs[n] for n in neighbours}

                if reversed:
                    target = max(with_costs.values())
                else:
                    target = min(with_costs.values())

                options = [k for k, v in with_costs.items() if v == target]
                return random.choice(options)
            else:
                return point

        # --
        if corner is not None:
            return next_one(self.graph_corners[corner], point, reversed)
        else:
            return next_one(self.graph_costs, point, reversed)

    # ########################################################################
    # ####################################################### CLEAR COSTS ####
    def clear_costs(self) -> None:
        """Useful on player death, otherwise enemies follow obsolete values"""
        self.graph_costs.clear()
