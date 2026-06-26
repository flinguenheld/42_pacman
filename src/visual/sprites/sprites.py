from __future__ import annotations

import arcade
import random
from typing import Any
from arcade import Sprite, SpriteList, Vec2

from src.visual import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class Sprites:
    def __init__(self, atlas: VAtlas, base_name: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList()
        self.base_name: str = base_name
        self.info: dict[str, Any] = {}
        self.atlas = atlas

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def add_sprite(
        self,
        texture_name: str,
        center: Vec2,
        scale: int,
        angle: int,
    ) -> None:

        texture = self._pick_texture(texture_name, False)

        if isinstance(texture, arcade.TextureAnimation):
            sprite = arcade.TextureAnimationSprite(
                animation=texture,
                center_x=center.x,
                center_y=center.y,
                scale=scale,
                angle=angle,
            )
        else:
            sprite = arcade.Sprite(
                path_or_texture=texture,
                center_x=center.x,
                center_y=center.y,
                scale=scale,
                angle=angle,
            )

        self.sprites.append(sprite)

    # ########################################################################
    # ###################################################### PICK TEXTURE ####
    def _pick_texture(self, who: str, first_more_probable: bool):

        if first_more_probable and random.randint(0, 10) < 7:
            return self.atlas.textures[who][0]

        return random.choice(self.atlas.textures[who])

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int) -> float:
        return VData.SPRITE_SIZE / size

    def update_animation(self, delta_time):
        self.sprites.update_animation(delta_time)
