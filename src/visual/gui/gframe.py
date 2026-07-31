import random
from typing import Tuple
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

    SEPARATOR_GAP = 4

    def __init__(
        self,
        atlas: VAtlas,
        nb_cols: int = 10,
        nb_rows: int = 10,
        bot_left: Vec2 = Vec2(0, 0),
        separators: list[int] = [],
        bevels: bool = False,
    ) -> None:

        self.separators = separators
        raw_maze = self.build_raw_maze(nb_rows, nb_cols, bevels)
        raw_maze = self.randomise_raw_maze(raw_maze)
        self.maze = Maze(atlas, raw_maze, floor_as_frame=True)
        self.maze.build(sprite_offset=bot_left)

    # ########################################################################
    # ########################################################## RAW MAZE ####
    def build_raw_maze(
        self,
        nb_rows: int,
        nb_cols: int,
        bevels: bool,
    ) -> list[list[int]]:
        """Create a simple raw maze which can be used as frame"""

        raw_maze: list[list[int]] = []
        BEVELS = self.get_bevels(bevels, nb_rows, nb_cols)
        BEVELS_SEP = self.get_bevels_separators(bevels, nb_cols)

        for row in range(nb_rows):
            new_row: list[int] = []
            for col in range(nb_cols):
                if col == 0 or col == nb_cols - 1:
                    new_row.append(1)
                elif row == 0 or row == nb_rows - 1:
                    new_row.append(1)
                elif (row, col) in BEVELS:
                    new_row.append(1)
                elif (row, col) in BEVELS_SEP:
                    new_row.append(0)
                elif (
                    row in self.separators
                    and col > GFrame.SEPARATOR_GAP
                    and col < nb_cols - GFrame.SEPARATOR_GAP - 1
                ):
                    new_row.append(1)
                else:
                    new_row.append(0)

            raw_maze.append(new_row)

        return raw_maze

    # ########################################################################
    # ############################################################ BEVELS ####
    def get_bevels(
        self,
        active: bool,
        nb_rows: int,
        nb_cols: int,
    ) -> set[Tuple[int, int]]:

        if not active:
            return set()

        return set(
            [
                (1, 1),
                (1, 2),
                (2, 1),
                (1, nb_cols - 2),
                (1, nb_cols - 3),
                (2, nb_cols - 2),
                (nb_rows - 2, nb_cols - 2),
                (nb_rows - 2, nb_cols - 3),
                (nb_rows - 3, nb_cols - 2),
                (nb_rows - 2, 1),
                (nb_rows - 2, 2),
                (nb_rows - 3, 1),
            ]
        )

    # ########################################################################
    # ################################################# BEVELS SEPARATORS ####
    def get_bevels_separators(
        self,
        active: bool,
        nb_cols: int,
    ) -> set[Tuple[int, int]]:
        """
        Loop in the separators to find consecutive ones.
        If there are, add their corners in the set.
        """

        GAP = GFrame.SEPARATOR_GAP + 1
        bevels: set[Tuple[int, int]] = set()

        if not active:
            return bevels

        # --
        def add_bevel_separator() -> None:
            if len(group) >= 3:
                bevels.add((group[0], GAP))
                bevels.add((group[0], nb_cols - GAP - 1))
                bevels.add((group[-1], GAP))
                bevels.add((group[-1], nb_cols - GAP - 1))

        # --
        group: list[int] = []
        for sep in self.separators:
            if not group:
                group.append(sep)
            elif group[-1] == sep - 1:
                group.append(sep)
            else:
                add_bevel_separator()

        add_bevel_separator()
        return bevels

    # ########################################################################
    # ######################################################### RANDOMISE ####
    def randomise_raw_maze(self, raw_maze: list[list[int]]) -> list[list[int]]:
        """Add some walls randomly"""

        for r, row in enumerate(raw_maze):
            for c, col in enumerate(row):
                if not col and random.randint(0, 150) == 42:
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
