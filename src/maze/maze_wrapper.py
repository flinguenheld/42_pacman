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
    EDGES: ClassVar[dict[str, int | Vec2]] = {
        "top_left": Vec2(0, 0),
        "top_right": Vec2(0, 0),
        "bot_right": Vec2(0, 0),
        "bot_left": Vec2(0, 0),
        "center": Vec2(0, 0),
    }

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

        def up_edges():

            to_world = Maze.to_world_coords

            maze_top = to_world(max(self.walls, key=lambda w: w.y)).y
            maze_right = to_world(max(self.walls, key=lambda w: w.x)).x
            maze_bot = to_world(min(self.walls, key=lambda w: w.y)).y
            maze_left = to_world(min(self.walls, key=lambda w: w.x)).x

            maze_top += VData.SPRITE_SIZE // 2
            maze_right += VData.SPRITE_SIZE // 2
            maze_bot -= VData.SPRITE_SIZE // 2
            maze_left -= VData.SPRITE_SIZE // 2

            Maze.EDGES["top_left"] = Vec2(maze_left, maze_top)
            Maze.EDGES["top_right"] = Vec2(maze_right, maze_top)
            Maze.EDGES["bot_left"] = Vec2(maze_left, maze_bot)
            Maze.EDGES["bot_right"] = Vec2(maze_right, maze_bot)
            Maze.EDGES["center"] = Vec2(
                maze_left + ((maze_right - maze_left) / 2),
                maze_bot + ((maze_top - maze_bot) / 2),
            )

        # --
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

        # --
        up_edges()

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

    # ########################################################################
    # ################################################### TO WORLD COORDS ####
    @classmethod
    def to_world_coords(cls, maze_pos: Vec2) -> Vec2:
        """Convert maze grid coordinates to world coordinates."""

        # shift_x = (VData.WIDTH - (cls.WIDTH * VData.SPRITE_SIZE * 2)) // 2
        # shift_y = (VData.HEIGHT - (cls.HEIGHT * VData.SPRITE_SIZE * 2)) // 2

        return Vec2(
            maze_pos.x * VData.SPRITE_SIZE,
            maze_pos.y * VData.SPRITE_SIZE,
        )
