from arcade import Vec2, LBWH, Rect

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░▀█▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░░█░░░█░░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class GTitle:
    def __init__(self, atlas: VAtlas, title_maze: list[list[int]]) -> None:
        self.atlas = atlas
        self.title_maze = title_maze

        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas)

        self.center = Vec2(0, 0)

    # ########################################################################
    # ###################################################### SET POSITION ####
    def set_postion(self, center_x: int, center_y: int) -> None:
        self.center = Vec2(center_x, center_y)
        self._build(center_x - self.width // 2, center_y - self.height // 2)

    # ########################################################################
    # ############################################################# SETUP ####
    def _build(self, offset_x: int, offset_y: int) -> None:
        wall_points: set[Vec2] = set()
        floor_points: set[Vec2] = set()

        sprite_size = VData.SPRITE_SIZE
        for y, row in enumerate(reversed(self.title_maze)):
            for x, value in enumerate(row):
                point = Vec2(
                    x * sprite_size + offset_x,
                    y * sprite_size + offset_y,
                )

                if value == 0:
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
    def width(self) -> int:
        return len(self.title_maze[0]) * VData.SPRITE_SIZE

    @property
    def height(self) -> int:
        return len(self.title_maze) * VData.SPRITE_SIZE

    @property
    def rect(self) -> Rect:
        return LBWH(
            self.center.x - self.width / 2,
            self.center.y - self.height / 2,
            self.width,
            self.height,
        )
