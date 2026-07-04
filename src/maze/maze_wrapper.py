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
        self._clear_edges()

    # ########################################################################
    # ################################################# GENERATE NEW MAZE ####
    def generate_new_maze(
        self,
        # TODO: RENAME RAW WIDTH
        # TODO: RENAME RAW WIDTH
        # TODO: RENAME RAW WIDTH
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

        def add_wall_and_up_edges(x: int, y: int):
            self._up_edges(x, y)
            self.walls.add(Vec2(x, y))

        # --
        self.walls.clear()

        sprite_size = VData.SPRITE_SIZE
        for raw_y, row in enumerate(reversed(self.raw_maze)):
            for raw_x, value in enumerate(row):
                # Get world coordinates --
                y = (raw_y * 2 + 1) * sprite_size
                x = (raw_x * 2 + 1) * sprite_size

                # --
                if value & 0b0001 == 0b0001:  # Top
                    add_wall_and_up_edges(x, y + sprite_size)
                    add_wall_and_up_edges(x - sprite_size, y + sprite_size)
                    add_wall_and_up_edges(x + sprite_size, y + sprite_size)

                if value & 0b0100 == 0b0100:  # Bottom
                    add_wall_and_up_edges(x, y - sprite_size)
                    add_wall_and_up_edges(x - sprite_size, y - sprite_size)
                    add_wall_and_up_edges(x + sprite_size, y - sprite_size)

                if value & 0b1000 == 0b1000:  # Left
                    add_wall_and_up_edges(x - sprite_size, y)
                    add_wall_and_up_edges(x - sprite_size, y - sprite_size)
                    add_wall_and_up_edges(x - sprite_size, y + sprite_size)

                if value & 0b0010 == 0b0010:  # Right
                    add_wall_and_up_edges(x + sprite_size, y)
                    add_wall_and_up_edges(x + sprite_size, y - sprite_size)
                    add_wall_and_up_edges(x + sprite_size, y + sprite_size)

    # ########################################################################
    # ################################################## BUILD BACKGROUND ####
    def build_background(self) -> None:
        self.background.clear()

        # TODO: Find a way to cover the screen
        if self.width > self.height:
            from_x = int(self._left - VData.CAMERA_MARGIN)
            to_x = int(self._right + VData.CAMERA_MARGIN)

            from_y = int(self._bot - (VData.HEIGHT))
            to_y = int(self._top + (VData.HEIGHT))

        else:
            from_y = int(self._bot - VData.CAMERA_MARGIN)
            to_y = int(self._top + VData.CAMERA_MARGIN)

            from_x = int(self._left - (VData.WIDTH))
            to_x = int(self._right + (VData.WIDTH))

        print(f"left: {self._left}")
        print(f"width: {self.width}")
        print(f"screen width: {VData.WIDTH}")
        print(f"{from_x}/{from_y}  ->  {to_x}/{to_y}")

        for x in range(from_x, to_x, VData.SPRITE_SIZE_BACKGROUND):
            for y in range(from_y, to_y, VData.SPRITE_SIZE_BACKGROUND):
                self.background.add(Vec2(x, y))

    # ########################################################################
    # ############################################################# EDGES ####
    def _clear_edges(self):
        self._top = 0.0
        self._bot = 0.0
        self._left = 0.0
        self._right = 0.0

    # def _up_edges(self, point: Vec2):
    def _up_edges(self, x: int, y: int):
        """
        Save the edges.
        Used while adding new sprites to avoid calculations.
        """
        if y < self._bot:
            self._bot = y
        if y > self._top:
            self._top = y

        if x < self._left:
            self._left = x
        if x > self._right:
            self._right = x

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self):
        center = Vec2(self._left + self.width / 2, self._bot + self.height / 2)
        return center

    @property
    def width(self):
        return self._right - self._left

    @property
    def height(self):
        return self._top - self._bot
