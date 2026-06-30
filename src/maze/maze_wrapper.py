from src.visual import VData
from itertools import count
from typing import ClassVar
from arcade import Vec2
from mazegenerator import MazeGenerator
from dataclasses import dataclass, field


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░
@dataclass
class Maze:
    WIDTH: ClassVar[int] = 15
    HEIGHT: ClassVar[int] = 10

    seed: int = 42
    entry: Vec2 = Vec2(1, 1)
    exit: Vec2 = Vec2(14, 14)
    walls: set[Vec2] = field(init=False, default_factory=set)
    floors: set[Vec2] = field(init=False, default_factory=set)
    forty_two: set[Vec2] = field(init=False, default_factory=set)
    raw_maze: list[list[int]] = field(init=False, default_factory=list)

    # ########################################################################
    # ################################################# GENERATE NEW MAZE ####
    def generate_new_maze(self) -> None:
        maze_gen = MazeGenerator(
            size=(Maze.WIDTH, Maze.HEIGHT),
            entry_cell=(int(self.entry.x), int(self.entry.y)),
            exit_cell=(int(self.exit.x), int(self.exit.y)),
            perfect=False,
            seed=self.seed,
        )
        self.entry = Vec2(maze_gen.maze_entry[0], maze_gen.maze_entry[1])
        self.exit = Vec2(maze_gen.maze_exit[0], maze_gen.maze_exit[1])
        self.raw_maze = maze_gen.maze

    # TODO: SET REAL COORDINATES HERE ??????? with the size ????????

    # ########################################################################
    # ###################################################### BUILD FLOORS ####
    def build_floors(self) -> None:
        self.floors.clear()
        for y in range(len(self.raw_maze) * 2):
            for x in range(len(self.raw_maze[0]) * 2):
                reversed_y = len(self.raw_maze) * 2 - y
                point = Vec2(x, reversed_y)

                # Keep fortytwo in its own set
                if x % 2 != 0 and y % 2 != 0:
                    if self.raw_maze[y // 2][x // 2] & 0b1111 == 0b1111:
                        self.forty_two.add(point)
                        continue

                if point not in self.walls:
                    self.floors.add(point)

    # ########################################################################
    # ################################################## BUILD BACKGROUND ####
    def background(self):

        blah = set()

        for x in range(VData.SPRITE_SIZE // 2, VData.WIDTH, VData.SPRITE_SIZE):
            for y in range(
                VData.SPRITE_SIZE // 2, VData.HEIGHT, VData.SPRITE_SIZE
            ):
                pt = Vec2(x, y)
                # if pt not in self.walls:
                # TODO NOT GOOD, PUT SPRITES WHERE IT'S USELESS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # TODO NOT GOOD, PUT SPRITES WHERE IT'S USELESS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # TODO NOT GOOD, PUT SPRITES WHERE IT'S USELESS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # TODO NOT GOOD, PUT SPRITES WHERE IT'S USELESS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                blah.add(Vec2(x, y))

        return blah

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
        self.walls.clear()

        # Loop in the maze draw where it's open
        for raw_y, row in enumerate(reversed(self.raw_maze)):
            for raw_x, value in enumerate(row):
                # Get real coordinates
                y = raw_y * 2 + 1
                x = raw_x * 2 + 1

                # --
                if value & 0b0001 == 0b0001:  # Top
                    self.walls.add(Vec2(x, y + 1))
                    self.walls.add(Vec2(x - 1, y + 1))
                    self.walls.add(Vec2(x + 1, y + 1))

                if value & 0b0100 == 0b0100:  # Bottom
                    self.walls.add(Vec2(x, y - 1))
                    self.walls.add(Vec2(x - 1, y - 1))
                    self.walls.add(Vec2(x + 1, y - 1))

                if value & 0b1000 == 0b1000:  # Left
                    self.walls.add(Vec2(x - 1, y))
                    self.walls.add(Vec2(x - 1, y - 1))
                    self.walls.add(Vec2(x - 1, y + 1))

                if value & 0b0010 == 0b0010:  # Right
                    self.walls.add(Vec2(x + 1, y))
                    self.walls.add(Vec2(x + 1, y - 1))
                    self.walls.add(Vec2(x + 1, y + 1))
