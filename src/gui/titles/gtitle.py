from arcade import Vec2, Rect

from src.maze.maze import Maze
from src.config.config import Config
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░▀█▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░░█░░░█░░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class GTitle:
    """
    Manage a maze to display a text.
    """

    def __init__(self, atlas: VAtlas, title_maze: list[list[int]]) -> None:
        self.maze = Maze(atlas, title_maze)
        self.raw_maze = title_maze

    # ########################################################################
    # ############################################################# BUILD ####
    def build(self, bottom_middle: Vec2) -> None:

        future_width = (len(self.raw_maze[0])) * Config.SPRITE_SIZE
        offset = Vec2(
            bottom_middle.x - future_width / 2 + Config.SPRITE_SIZE / 2,
            bottom_middle.y,
        )

        self.maze.build(sprite_offset=offset)

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
