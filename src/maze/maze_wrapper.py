from arcade import Vec2
from typing import ClassVar
from src.visual import VData
from mazegenerator import MazeGenerator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class Maze:
    WIDTH: ClassVar[int] = 15
    HEIGHT: ClassVar[int] = 15

    def __init__(self):
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self):
        self.walls: set[Vec2] = set()
        self.floors: set[Vec2] = set()
        self.forty_two: set[Vec2] = set()
        self.background: set[Vec2] = set()
        self.raw_maze: list[list[int]] = list()

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
            exit(15)
        else:
            Maze.WIDTH = width
            Maze.HEIGHT = height

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
    def build_background(self) -> None:

        try:
            self.background.clear()
            top = Maze.to_world_coords(max(self.walls, key=lambda w: w.y))
            right = Maze.to_world_coords(max(self.walls, key=lambda w: w.x))
            bot = Maze.to_world_coords(min(self.walls, key=lambda w: w.y))
            left = Maze.to_world_coords(min(self.walls, key=lambda w: w.x))

        except ValueError:
            top = right = bot = left = Vec2(0, 0)

        sprite_size = VData.SPRITE_SIZE
        for x in range(0, VData.WIDTH + sprite_size, sprite_size):
            for y in range(0, VData.HEIGHT + sprite_size, sprite_size):
                if x > left.x and x < right.x and y > bot.y and y < top.y:
                    continue

                self.background.add(Vec2(x, y))

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

    # ########################################################################
    # ################################################### TO WORLD COORDS ####
    @classmethod
    def to_world_coords(cls, maze_pos: Vec2, scale: float = 2.0) -> Vec2:
        """Convert maze grid coordinates to world coordinates."""

        shift_x = (VData.WIDTH - (cls.WIDTH * VData.SPRITE_SIZE * 2)) // 2
        shift_y = (VData.HEIGHT - (cls.HEIGHT * VData.SPRITE_SIZE * 2)) // 2

        return Vec2(
            maze_pos.x * VData.SPRITE_SIZE + shift_x,
            maze_pos.y * VData.SPRITE_SIZE + shift_y,
        )
