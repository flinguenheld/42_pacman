from __future__ import annotations
import time
import random

from arcade import Vec2
from src.visual.sprites.sprites import Sprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▄█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class SWall(Sprites):
    def __init__(self) -> None:
        super().__init__("wall")

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, walls: set[Vec2], floors: set[Vec2]) -> None:

        self.reload_info()

        for point in walls:
            is_floor_top = Vec2(point.x, point.y + 1) in floors
            is_floor_right = Vec2(point.x + 1, point.y) in floors
            is_floor_bot = Vec2(point.x, point.y - 1) in floors
            is_floor_left = Vec2(point.x - 1, point.y) in floors

            filename = "full"
            random.seed(time.time())
            angle = random.choice([0, 90, 180, 270])

            match (is_floor_top, is_floor_right, is_floor_bot, is_floor_left):
                case (False, False, True, False):
                    filename = "simple"
                    angle = 0
                case (False, False, False, True):
                    filename = "simple"
                    angle = 90
                case (True, False, False, False):
                    filename = "simple"
                    angle = 180
                case (False, True, False, False):
                    filename = "simple"
                    angle = 270

                # --
                case (True, False, True, False):
                    filename = "corridor"
                    angle = random.choice([0, 180])
                case (False, True, False, True):
                    filename = "corridor"
                    angle = random.choice([90, 270])

                # --
                case (True, True, False, True):
                    filename = "end"
                    angle = 0
                case (True, True, True, False):
                    filename = "end"
                    angle = 90
                case (False, True, True, True):
                    filename = "end"
                    angle = 180
                case (True, False, True, True):
                    filename = "end"
                    angle = 270

                # --
                case (True, True, False, False):
                    filename = "angle"
                    angle = 0
                case (False, True, True, False):
                    filename = "angle"
                    angle = 90
                case (False, False, True, True):
                    filename = "angle"
                    angle = 180
                case (True, False, False, True):
                    filename = "angle"
                    angle = 270

            self.add_sprite(point, filename, angle)

            # --
            self.add_extra_angles(point, walls, floors)

    # ########################################################################
    # ###################################################### EXTRA ANGLES ####
    def add_extra_angles(self, point: Vec2, walls, floors) -> None:
        is_floor_top_left = Vec2(point.x - 1, point.y + 1) in floors
        is_floor_top_right = Vec2(point.x + 1, point.y + 1) in floors
        is_floor_bot_left = Vec2(point.x - 1, point.y - 1) in floors
        is_floor_bot_right = Vec2(point.x + 1, point.y - 1) in floors

        is_wall_top = Vec2(point.x, point.y + 1) in walls
        is_wall_right = Vec2(point.x + 1, point.y) in walls
        is_wall_bot = Vec2(point.x, point.y - 1) in walls
        is_wall_left = Vec2(point.x - 1, point.y) in walls

        if is_wall_bot and is_wall_left and is_floor_bot_left:
            self.add_sprite(point, "special", 0)

        if is_wall_top and is_wall_left and is_floor_top_left:
            self.add_sprite(point, "special", 90)

        if is_wall_top and is_wall_right and is_floor_top_right:
            self.add_sprite(point, "special", 180)

        if is_wall_bot and is_wall_right and is_floor_bot_right:
            self.add_sprite(point, "special", 270)
