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
    walls: dict[Vec2, str] = field(init=False, default_factory=dict)
    paths: set[Vec2] = field(init=False, default_factory=set)
    forty_two: set[Vec2] = field(init=False, default_factory=set)
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
    # ######################################################## BUILD PATH ####
    def build_path(self):

        for raw_y, row in enumerate(reversed(self.raw_maze)):
            for raw_x, value in enumerate(row):
                # Get real coordinates
                y = raw_y * 2 + 1
                x = raw_x * 2 + 1

        for y in range(len(self.raw_maze) * 2):
            for x in range(len(self.raw_maze[0]) * 2):
                # Reverse -_-'
                rev_y = len(self.raw_maze) * 2 - y

                point = Vec2(x, rev_y)

                # Do not add 42
                if x % 2 != 0 and y % 2 != 0:
                    if self.raw_maze[y // 2][x // 2] & 0b1111 == 0b1111:
                        self.forty_two.add(point)
                        continue

                if point not in self.walls:
                    self.paths.add(point)

    # ########################################################################
    # ######################################################## BUILD MAZE ####
    def build_walls(self) -> None:
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

        def add_maze_entry(where: Vec2, what: str) -> None:
            """Add what in where and sort letters"""
            if where in self.walls:
                if what not in self.walls[where]:
                    self.walls[where] += what
                    self.walls[where] = "".join(sorted(self.walls[where]))
            else:
                self.walls[where] = what

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
