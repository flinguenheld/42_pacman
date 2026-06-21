from arcade import Vec2
from mazegenerator import MazeGenerator
from dataclasses import dataclass, field


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░
@dataclass
class Maze:
    seed: int = 42
    size: Vec2 = Vec2(15, 15)
    maze: dict[Vec2, str] = field(init=False, default_factory=dict)
    raw_maze: list[list[int]] = field(init=False, default_factory=list)

    # ########################################################################
    # ################################################# GENERATE NEW MAZE ####
    def generate_new_maze(self) -> None:
        self.raw_maze = MazeGenerator(
            size=(int(self.size.x), int(self.size.y)),
            perfect=False,
            seed=self.seed,
        ).maze

    # ########################################################################
    # ######################################################## BUILD MAZE ####
    def build_maze(self) -> None:

        def add_maze_entry(where: Vec2, what: str) -> None:
            """Add what in where and sort letters"""
            if where in self.maze:
                if what not in self.maze[where]:
                    self.maze[where] += what
                    self.maze[where] = "".join(sorted(self.maze[where]))
            else:
                self.maze[where] = what

        """
        Loop in the raw maze to fill maze
        !! Arcade works from bottom left with X, Y !!
        !! Reverse the logic !!
        !! Reverse on Y !!

        raw ->        0       1       2       3       4
         |
         v        0   1   2   3   4   5   6   7   8   9  10

                ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
             0  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         0   1  ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             2  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         1   3  ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             4  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         2   5  ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             6  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
        """

        # Loop in the maze draw where it's open
        for raw_y, row in enumerate(reversed(self.raw_maze)):
            for raw_x, value in enumerate(row):
                # Get real coordinates
                y = raw_y * 2 + 1
                x = raw_x * 2 + 1

                # --
                if value & 0b0001 == 0b0001:  # Top
                    add_maze_entry(Vec2(x, y + 1), "LR")
                    add_maze_entry(Vec2(x - 1, y + 1), "R")
                    add_maze_entry(Vec2(x + 1, y + 1), "L")

                if value & 0b0100 == 0b0100:  # Bottom
                    add_maze_entry(Vec2(x, y - 1), "LR")
                    add_maze_entry(Vec2(x - 1, y - 1), "R")
                    add_maze_entry(Vec2(x + 1, y - 1), "L")

                if value & 0b1000 == 0b1000:  # Left
                    add_maze_entry(Vec2(x - 1, y), "BT")
                    add_maze_entry(Vec2(x - 1, y - 1), "T")
                    add_maze_entry(Vec2(x - 1, y + 1), "B")

                if value & 0b0010 == 0b0010:  # Right
                    add_maze_entry(Vec2(x + 1, y), "BT")
                    add_maze_entry(Vec2(x + 1, y - 1), "T")
                    add_maze_entry(Vec2(x + 1, y + 1), "B")
