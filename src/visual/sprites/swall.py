from src.utils.maze_grid_to_world_coords import maze_grid_to_world_coords
import random
from arcade import Vec2
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

        for point in walls:
            is_floor_top = Vec2(point.x, point.y + 1) in floors
            is_floor_right = Vec2(point.x + 1, point.y) in floors
            is_floor_bot = Vec2(point.x, point.y - 1) in floors
            is_floor_left = Vec2(point.x - 1, point.y) in floors

            texture_name = "full"
            angle = random.choice([0, 90, 180, 270])
            point_world = maze_grid_to_world_coords(point)

            match (is_floor_top, is_floor_right, is_floor_bot, is_floor_left):
                case (False, False, True, False):
                    texture_name = "simple"
                    angle = 0
                case (False, False, False, True):
                    texture_name = "simple"
                    angle = 90
                case (True, False, False, False):
                    texture_name = "simple"
                    angle = 180
                case (False, True, False, False):
                    texture_name = "simple"
                    angle = 270

                # --
                case (True, False, True, False):
                    texture_name = "corridor"
                    angle = random.choice([0, 180])
                case (False, True, False, True):
                    texture_name = "corridor"
                    angle = random.choice([90, 270])

                # --
                case (True, True, False, True):
                    texture_name = "end"
                    angle = 0
                case (True, True, True, False):
                    texture_name = "end"
                    angle = 90
                case (False, True, True, True):
                    texture_name = "end"
                    angle = 180
                case (True, False, True, True):
                    texture_name = "end"
                    angle = 270

                # --
                case (True, True, False, False):
                    texture_name = "angle"
                    angle = 0
                case (False, True, True, False):
                    texture_name = "angle"
                    angle = 90
                case (False, False, True, True):
                    texture_name = "angle"
                    angle = 180
                case (True, False, False, True):
                    texture_name = "angle"
                    angle = 270

            # TODO: ADD SCALE ###############################################
            self.add_sprite(
                f"{self.base_name}{texture_name}", point_world, 2, angle
            )

            # --
            # self.add_extra_angles(point, walls, floors)

    # ########################################################################
    # ###################################################### EXTRA ANGLES ####
    def add_extra_angles(
        self,
        point: Vec2,
        walls: set[Vec2],
        floors: set[Vec2],
    ) -> None:
        is_floor_top_left = Vec2(point.x - 1, point.y + 1) in floors
        is_floor_top_right = Vec2(point.x + 1, point.y + 1) in floors
        is_floor_bot_left = Vec2(point.x - 1, point.y - 1) in floors
        is_floor_bot_right = Vec2(point.x + 1, point.y - 1) in floors

        is_wall_top = Vec2(point.x, point.y + 1) in walls
        is_wall_right = Vec2(point.x + 1, point.y) in walls
        is_wall_bot = Vec2(point.x, point.y - 1) in walls
        is_wall_left = Vec2(point.x - 1, point.y) in walls

        # if is_wall_bot and is_wall_left and is_floor_bot_left:
        #     self.add_sprite(point, "special", 0)

        # if is_wall_top and is_wall_left and is_floor_top_left:
        #     self.add_sprite(point, "special", 90)

        # if is_wall_top and is_wall_right and is_floor_top_right:
        #     self.add_sprite(point, "special", 180)

        # if is_wall_bot and is_wall_right and is_floor_bot_right:
        #     self.add_sprite(point, "special", 270)
