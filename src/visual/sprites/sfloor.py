from arcade import Vec2
from src.visual.vatlas import VAtlas
from src.visual.sprites.ssprites import SSprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█░░░█▀█░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█░░░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class SFloor(SSprites):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(atlas, "floor_")

    def reload(self, floors: set[Vec2]) -> None:

        self.clear()
        for point in floors:
            self.add_sprite(f"{self.base_name}full", center=point)
