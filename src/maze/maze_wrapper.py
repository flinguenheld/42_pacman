from __future__ import annotations

from arcade import Vec2
from src.visual.vdata import VData
from mazegenerator import MazeGenerator


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
        raw_width: int = 15,
        raw_height: int = 15,
        seed: int = 42,
    ) -> None:

        try:
            maze_gen = MazeGenerator(
                size=(raw_width, raw_height),
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

        def add_wall_and_up_edges(x: int, y: int) -> None:
            self._up_edges(x, y)
            self.walls.add(Vec2(x, y))

        # --
        self.walls.clear()
        self._clear_edges()

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

        # Simple and oversized
        from_x = self.left - VData.width // 2
        to_x = self.right + VData.width // 2
        from_y = self.bot - VData.height // 2
        to_y = self.top + VData.height // 2

        for x in range(from_x, to_x, VData.SPRITE_SIZE_BACKGROUND):
            for y in range(from_y, to_y, VData.SPRITE_SIZE_BACKGROUND):
                self.background.add(Vec2(x, y))

    # ########################################################################
    # ############################################################# EDGES ####
    def _clear_edges(self) -> None:
        """
        Edges are the center of tiles which are on max of top/bot/left/right.
        """
        self.top = 0
        self.bot = 0
        self.left = 0
        self.right = 0

    def _up_edges(self, x: int, y: int) -> None:
        """
        Save the edges.
        Used while building walls to avoid calculations.
        """
        # QUESTION: Since we use the real coordinates, left and bot are 0
        # QUESTION: So keep them ???

        # if y < self.bot:
        #     self.bot = y
        if y > self.top:
            self.top = y

        # if x < self.left:
        #     self.left = x
        if x > self.right:
            self.right = x

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self) -> Vec2:
        center = Vec2(self.left + self.width / 2, self.bot + self.height / 2)
        return center

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.top - self.bot

    # ########################################################################
    # ##################################################### FLOOR CORNERS ####
    @property
    def floor_corners(self) -> list[Vec2]:
        """Return floor corners:  left/bot, left/top, right/top, right/bot."""

        bot = VData.SPRITE_SIZE
        top = self.top - VData.SPRITE_SIZE
        left = VData.SPRITE_SIZE
        right = self.width - VData.SPRITE_SIZE

        return [
            Vec2(left, bot),
            Vec2(left, top),
            Vec2(right, top),
            Vec2(right, bot),
        ]

    # ########################################################################
    # ###################################################### FLOOR CENTER ####
    @property
    def floor_center(self) -> Vec2:
        """Center of the floor which is the closest to the maze center."""

        y = self.center_position.y
        middle_row = [f for f in self.floors if f.y == y]
        middle_row.sort(key=lambda pt: pt.x)

        maze_center = self.center_position.x - VData.SPRITE_SIZE
        for pt in middle_row:
            if pt.x >= maze_center:
                return pt

        return Vec2(VData.SPRITE_SIZE, VData.SPRITE_SIZE)
