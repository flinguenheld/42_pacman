import arcade
import random
from arcade import Sprite, SpriteList, Vec2

from src.visual import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class SSprites:
    def __init__(self, atlas: VAtlas, base_name: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList(use_spatial_hash=True)
        self.base_name: str = base_name
        self.atlas = atlas

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def add_sprite(
        self,
        texture_name: str,
        center: Vec2,
        force_first_texture: bool = False,
        sprite_size: int = VData.SPRITE_SIZE,
    ) -> None:
        tile = self.atlas.pick_tile(texture_name, not force_first_texture)
        angle = random.choice(tile.allowed_angles)

        if isinstance(tile.texture, arcade.TextureAnimation):
            sprite_animation: Sprite = arcade.TextureAnimationSprite(
                animation=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=self._get_scale(tile.width, sprite_size),
            )
            sprite_animation.angle = angle
            self.sprites.append(sprite_animation)
        else:
            self.sprites.append(
                arcade.Sprite(
                    path_or_texture=tile.texture,
                    center_x=center.x,
                    center_y=center.y,
                    scale=self._get_scale(tile.width, sprite_size),
                    angle=angle,
                )
            )

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int, sprite_size: int) -> float:
        return sprite_size / size

    # ########################################################################
    # ############################################################# CLEAR ####
    def clear(self) -> None:
        self.sprites.clear()

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update_animation(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)
