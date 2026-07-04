from __future__ import annotations

from arcade import Vec2
from typing import ClassVar
from src.visual import VData
from mazegenerator import MazeGenerator

# TODO: KEEP "THE REAL" coordinates or use only real ones ???????
# TODO: KEEP "THE REAL" coordinates or use only real ones ???????
# TODO: KEEP "THE REAL" coordinates or use only real ones ???????
# TODO: KEEP "THE REAL" coordinates or use only real ones ???????
# TODO: KEEP "THE REAL" coordinates or use only real ones ???????


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class Maze:
    # TODO: CHANGE CASE ???
    # TODO: CHANGE CASE ???
    WIDTH: ClassVar[int] = 15
    HEIGHT: ClassVar[int] = 15

    def __init__(self) -> None:
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.walls: set[Vec2] = set()
        self.floors: set[Vec2] = set()
        self.forty_two: set[Vec2] = set()
        self.background: set[Vec2] = set()
        self.raw_maze: list[list[int]] = list()
        self.edges: dict[str, int] = {}

    # ########################################################################
    # ################################################# GENERATE NEW MAZE ####
    def generate_new_maze(
        self,
        width: int = 15,
        height: int = 15,
        seed: int = 42,
    ) -> None:

        try:
            maze_gen = MazeGenerator(
                size=(width, height),
                perfect=False,
                seed=seed,
            )
            self.setup()
            self.raw_maze = maze_gen.maze
        except RecursionError:
            # TODO: add something ????
            exit(42)
        else:
            Maze.WIDTH = width
            Maze.HEIGHT = height

    # ########################################################################
    # ###################################################### BUILD FLOORS ####
    def build_floors(self) -> None:
        self.floors.clear()
        self.forty_two.clear()
        for y in range(len(self.raw_maze) * 2):
            for x in range(len(self.raw_maze[0]) * 2):
                reversed_y = len(self.raw_maze) * 2 - y
                point = Vec2(x, reversed_y)
                point *= VData.SPRITE_SIZE

                # Keep fortytwo in its own set
                if x % 2 != 0 and y % 2 != 0:
                    if self.raw_maze[y // 2][x // 2] & 0b1111 == 0b1111:
                        self.forty_two.add(point)
                        continue

                if point not in self.walls:
                    self.floors.add(point)

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
         v        0   32  64  96 128 160 192 224 256 288 320

                ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
             0  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         0   32 ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             64 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         1   96 ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
            128 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         2  192 ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
            224 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
        """

        # --
        self.walls.clear()

        # Loop in the maze draw where it's open
        for raw_y, row in enumerate(reversed(self.raw_maze)):
            for raw_x, value in enumerate(row):
                SS = VData.SPRITE_SIZE
                # Get world coordinates --
                y = (raw_y * 2 + 1) * SS
                x = (raw_x * 2 + 1) * SS

                # --
                if value & 0b0001 == 0b0001:  # Top
                    self.walls.add(Vec2(x, y + SS))
                    self.walls.add(Vec2(x - SS, y + SS))
                    self.walls.add(Vec2(x + SS, y + SS))

                if value & 0b0100 == 0b0100:  # Bottom
                    self.walls.add(Vec2(x, y - SS))
                    self.walls.add(Vec2(x - SS, y - SS))
                    self.walls.add(Vec2(x + SS, y - SS))

                if value & 0b1000 == 0b1000:  # Left
                    self.walls.add(Vec2(x - SS, y))
                    self.walls.add(Vec2(x - SS, y - SS))
                    self.walls.add(Vec2(x - SS, y + SS))

                if value & 0b0010 == 0b0010:  # Right
                    self.walls.add(Vec2(x + SS, y))
                    self.walls.add(Vec2(x + SS, y - SS))
                    self.walls.add(Vec2(x + SS, y + SS))

    # ########################################################################
    # ################################################## BUILD BACKGROUND ####
    def build_background(self) -> None:
        self.background.clear()

        # horizontal = (VData.WIDTH - Maze.WIDTH) // 2
        # vertical = (VData.HEIGHT - Maze.HEIGHT) // 2

        # from_x = Maze.EDGES["left"] - horizontal
        # to_x = Maze.EDGES["right"] + horizontal

        # from_y = Maze.EDGES["bot"] - vertical
        # to_y = Maze.EDGES["top"] + vertical

        # for x in range(from_x, to_x, VData.SPRITE_SIZE_BACKGROUND):
        #     for y in range(from_y, to_y, VData.SPRITE_SIZE_BACKGROUND):
        #         self.background.add(Vec2(x, y))
