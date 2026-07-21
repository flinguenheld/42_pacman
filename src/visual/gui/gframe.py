import random
from arcade import Vec2, Rect

from src.maze.maze import Maze
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█▀▄░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀▄░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀░▀░▀░▀░▀▀▀░░
class GFrame:
    """
    Create and manage a maze to display a frame.
    """

    def __init__(
        self,
        atlas: VAtlas,
        nb_cols: int = 10,
        nb_rows: int = 10,
        bot_left: Vec2 = Vec2(0, 0),
        separators: list[int] = [],
    ) -> None:

        raw_maze = self.build_raw_maze(nb_rows, nb_cols, separators)
        raw_maze = self.randomise_raw_maze(raw_maze)
        self.maze = Maze(atlas, raw_maze, floor_as_frame=True)
        self.maze.build_sprites(offset=bot_left)

    # ########################################################################
    # ########################################################## RAW MAZE ####
    def build_raw_maze(
        self,
        nb_rows: int,
        nb_cols: int,
        separators: list[int],
    ) -> list[list[int]]:
        """Create a simple raw maze which can be used as frame"""

        raw_maze: list[list[int]] = []
        for y in range(nb_rows):
            row: list[int] = []
            for x in range(nb_cols):
                if x == 0 or x == nb_cols - 1:
                    row.append(1)
                elif y == 0 or y == nb_rows - 1:
                    row.append(1)
                elif y in separators:
                    row.append(1)
                else:
                    row.append(0)

            raw_maze.append(row)

        return raw_maze

    # ########################################################################
    # ######################################################### RANDOMISE ####
    def randomise_raw_maze(self, raw_maze: list[list[int]]):
        """Add some walls randomly"""

        for r, row in enumerate(raw_maze):
            for c, col in enumerate(row):
                if not col and random.randint(0, 100) <= 1:
                    raw_maze[r][c] = not col

        return raw_maze

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
    def center_position(self) -> Vec2:
        return self.maze.center_position

    @property
    def rect(self) -> Rect:
        return self.maze.rect

    @property
    def height(self) -> int:
        return self.maze.height

    @property
    def width(self) -> int:
        return self.maze.width
