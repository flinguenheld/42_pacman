import arcade
from arcade import Vec2

from src.visual import VData
from src.visual.vatlas import VAtlas
from src.visual.entities.ventity_sprite import VEntitySprite


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░
class VEntity(VEntitySprite):
    def __init__(self, atlas: VAtlas, sprite_name: str, position: Vec2):
        self._atlas: VAtlas = atlas
        self._sprite_name = sprite_name

        self.init_sprite(position)
        self.position = position

    # ########################################################################
    # ####################################################### INIT SPRITE ####
    def init_sprite(self, position: Vec2) -> None:

        tile = self._atlas.pick_tile(
            f"{self._sprite_name}_wait",
            randomly=True,
        )

        if not isinstance(tile.texture, arcade.TextureAnimation):
            raise ValueError("The given texture has to be animated.")

        super().__init__(
            animation=tile.texture,
            center=position,
            scale=tile.width / VData.SPRITE_SIZE,
        )
