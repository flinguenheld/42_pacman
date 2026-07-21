from arcade import Vec2, Rect

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░▀█▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░░█░░░█░░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class GTitle:
    """
    Manage a maze to display a text.
    """

    def __init__(self, atlas: VAtlas, title_maze: list[list[int]]) -> None:
        self.maze = Maze(atlas, title_maze)

        self.future_width = len(title_maze[0]) * VData.SPRITE_SIZE
        self.future_height = len(title_maze) * VData.SPRITE_SIZE

    # ########################################################################
    # ############################################################# BUILD ####
    def build(self, center: Vec2):
        center = Vec2(
            center.x - self.future_width / 2,
            center.y - self.future_height / 2,
        )

        self.maze.build_sprites(offset=center)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.maze.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.maze.update(delta_time)

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def width(self) -> int:
        return self.maze.width

    @property
    def height(self) -> int:
        return self.maze.height

    @property
    def rect(self) -> Rect:
        return self.maze.rect
