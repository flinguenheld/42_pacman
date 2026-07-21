from arcade import Vec2, Rect

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class Maze:
    """
    Maze class
    From a raw maze list[list[int]] where:
        - 0 -> floor
        - 1 -> wall

    Build and manage two sprite_lists.
    Use sprite_lists properties for the maze such as center_position or rect...
    """

    def __init__(
        self,
        atlas: VAtlas,
        raw_maze: list[list[int]],
        floor_as_frame: bool = False,
    ) -> None:
        self.raw_maze = raw_maze
        self.atlas = atlas

        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas, frame_texture=floor_as_frame)

    # ########################################################################
    # ############################################################# SETUP ####
    def build_sprites(self, offset: Vec2 = Vec2(0, 0)) -> None:
        wall_points: set[Vec2] = set()
        floor_points: set[Vec2] = set()

        sprite_size = VData.SPRITE_SIZE
        # QUESTION: WHY REVERSED ????????????????????????????????????
        # QUESTION: WHY REVERSED ????????????????????????????????????
        # for y, row in enumerate(reversed(self.raw_maze)):
        for y, row in enumerate(self.raw_maze):
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

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.walls.draw()
        self.floors.draw()

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
        return self.floors.sprites_corners
