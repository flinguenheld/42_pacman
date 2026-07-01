from arcade import Vec2
from functools import partial
from src.visual.vatlas import VAtlas
from src.visual.sprites.sprites import Sprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▄█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class SWall(Sprites):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(atlas, "wall_")

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, walls: set[Vec2], floors: set[Vec2]) -> None:
        self.clear()

        # ############################### EXTRA ANGLES ###
        def will_have_extra_angle() -> bool:
            """Has to be checked first due to sprite transparency order"""
            if is_wall_on_bot and is_wall_on_left and is_floor_on_bot_left:
                return True
            if is_wall_on_top and is_wall_on_left and is_floor_on_top_left:
                return True
            if is_wall_on_top and is_wall_on_right and is_floor_on_top_right:
                return True
            if is_wall_on_bot and is_wall_on_right and is_floor_on_bot_right:
                return True
            return False

        def add_extra_angles() -> None:
            add = partial(self.add_sprite, center=point)

            if is_wall_on_bot and is_wall_on_left and is_floor_on_bot_left:
                add(texture_name=f"{self.base_name}extra_corner_bot_left")

            if is_wall_on_top and is_wall_on_left and is_floor_on_top_left:
                add(texture_name=f"{self.base_name}extra_corner_top_left")

            if is_wall_on_top and is_wall_on_right and is_floor_on_top_right:
                add(texture_name=f"{self.base_name}extra_corner_top_right")

            if is_wall_on_bot and is_wall_on_right and is_floor_on_bot_right:
                add(texture_name=f"{self.base_name}extra_corner_bot_right")

        # ##########################################
        # ################################################
        for point in walls:
            is_floor_on_top = Vec2(point.x, point.y + 1) in floors
            is_floor_on_right = Vec2(point.x + 1, point.y) in floors
            is_floor_on_bot = Vec2(point.x, point.y - 1) in floors
            is_floor_on_left = Vec2(point.x - 1, point.y) in floors

            is_floor_on_top_left = Vec2(point.x - 1, point.y + 1) in floors
            is_floor_on_top_right = Vec2(point.x + 1, point.y + 1) in floors
            is_floor_on_bot_left = Vec2(point.x - 1, point.y - 1) in floors
            is_floor_on_bot_right = Vec2(point.x + 1, point.y - 1) in floors

            is_wall_on_top = Vec2(point.x, point.y + 1) in walls
            is_wall_on_right = Vec2(point.x + 1, point.y) in walls
            is_wall_on_bot = Vec2(point.x, point.y - 1) in walls
            is_wall_on_left = Vec2(point.x - 1, point.y) in walls

            # --
            # point_world = maze_grid_to_world_coords(point)
            texture_name = "with_floor_on"

            if is_floor_on_top:
                texture_name += "_top"
            if is_floor_on_right:
                texture_name += "_right"
            if is_floor_on_bot:
                texture_name += "_bottom"
            if is_floor_on_left:
                texture_name += "_left"

            if texture_name == "with_floor_on":
                texture_name = "open_full"

            self.add_sprite(
                f"{self.base_name}{texture_name.removeprefix('_')}",
                center=point,
                force_first_texture=will_have_extra_angle(),
            )

            # --
            add_extra_angles()
