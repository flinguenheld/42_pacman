from src.visual import VData
import arcade
from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity_sprite import VEntitySprite


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░
class VEntity:
    def __init__(self, atlas: VAtlas, sprite_name: str, position: Vec2):
        self._atlas: VAtlas = atlas
        self._sprite_name = sprite_name

        self.init_sprite(position)
        self.position = position

    # ########################################################################
    # ########################################################## POSITION ####
    @property
    def position(self) -> Vec2:
        return Vec2(self.sprite.center_x, self.sprite.center_y)

    @position.setter
    def position(self, where: Vec2) -> None:
        self.sprite.center_x = where.x
        self.sprite.center_y = where.y

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.sprite.update_animation(delta_time)

    # ########################################################################
    # ####################################################### INIT SPRITE ####
    def init_sprite(self, position: Vec2) -> None:
        tile = self._atlas.textures[f"{self._sprite_name}_wait"][0]

        if not isinstance(tile.texture, arcade.TextureAnimation):
            raise ValueError("The given texture has to be animated.")

        self.sprite = VEntitySprite(
            animation=tile.texture,
            center=position,
            scale=tile.width / VData.SPRITE_SIZE,
        )
