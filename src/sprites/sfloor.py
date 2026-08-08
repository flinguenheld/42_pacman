from arcade import Vec2
from src.sprites.vatlas import VAtlas
from src.sprites.ssprites import SSprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█░░░█▀█░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█░░░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class SFloor(SSprites):
    def __init__(self, atlas: VAtlas, frame_texture: bool = False) -> None:
        base_name = "frame" if frame_texture else "floor"
        super().__init__(atlas, base_name)

    def reload(self, floors: set[Vec2]) -> None:
        """
        Reload the sprites.
        Has to be done for each new maze.
        """
        self.clear()
        for point in floors:
            self.add_sprite(self.base_name, center=point)
