from arcade import Vec2

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor


class GTitle:
    def __init__(
        self,
        atlas: VAtlas,
        title_maze: list[list[int]],
        center_x: int,
        bottom_y: int,
    ) -> None:
        self.atlas = atlas
        self.title = title_maze

        self.offset_x = center_x - (len(title_maze[0]) / 2 * VData.SPRITE_SIZE)
        self.setup(title_maze)

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self, title: list[list[int]]) -> None:
        wall_points: set[Vec2] = set()
        floor_points: set[Vec2] = set()

        sprite_size = VData.SPRITE_SIZE
        for y, row in enumerate(reversed(title)):
            for x, value in enumerate(row):
                point = Vec2(x * sprite_size + self.offset_x, y * sprite_size)

                if value == 0:
                    wall_points.add(point)
                else:
                    floor_points.add(point)

        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas)

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
