from arcade import Vec2
from src.visual.vatlas import VAtlas
from src.visual.sprites.sprites import Sprites
from src.utils.maze_grid_to_world_coords import maze_grid_to_world_coords


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█░░░█▀█░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█░░░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class SFloor(Sprites):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(atlas, "floor_")

    def reload(self, floors: set[Vec2]) -> None:

        self.clear()
        for point in floors:
            # point_world = maze_grid_to_world_coords(point)
            self.add_sprite(f"{self.base_name}full", point, 2)
