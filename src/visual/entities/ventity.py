import arcade
from arcade import Vec2, TextureAnimationSprite

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░
class VEntity(TextureAnimationSprite):
    def __init__(self, atlas: VAtlas, sprite_name: str, position: Vec2):
        self._atlas: VAtlas = atlas
        self._sprite_name = sprite_name

        self._init_sprite(position)
        self.position = position

    # ########################################################################
    # ####################################################### INIT SPRITE ####
    def _init_sprite(self, position: Vec2) -> None:

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
