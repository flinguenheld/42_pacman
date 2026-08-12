import arcade
from arcade import Vec2, TextureAnimationSprite

from src.config.config import Config
from src.sprites.vatlas import VAtlas


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
            raise TypeError("The given texture has to be animated.")

        super().__init__(
            animation=tile.texture,
            center=position,
            scale=tile.width / Config.SPRITE_SIZE,
        )

    # ########################################################################
    # ########################################## OVERRIDE CENTER POSITION ####
    @property
    def center(self) -> Vec2:
        """
        Override of Sprite.position to return Vec2 instead of Point2
        """
        return Vec2(self.center_x, self.center_y)

    @center.setter
    def center(self, new_pos: Vec2) -> None:
        self.center_x = new_pos.x
        self.center_y = new_pos.y
