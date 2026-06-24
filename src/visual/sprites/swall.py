from __future__ import annotations

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

            filename = ""

            if is_floor_bot:
                filename += "B"
            if is_floor_left:
                filename += "L"
            if is_floor_right:
                filename += "R"
            if is_floor_top:
                filename += "T"

            if not filename:
                filename = "wall"

            self.add_sprite(point, filename)

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

        if is_wall_top and is_wall_left and is_floor_top_left:
            self.add_sprite(point, "angle_LT")

        if is_wall_top and is_wall_right and is_floor_top_right:
            self.add_sprite(point, "angle_RT")

        if is_wall_bot and is_wall_left and is_floor_bot_left:
            self.add_sprite(point, "angle_BL")

        if is_wall_bot and is_wall_right and is_floor_bot_right:
            self.add_sprite(point, "angle_BR")
