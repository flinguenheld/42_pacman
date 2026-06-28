from __future__ import annotations

import arcade
import random
from typing import Any
from arcade import Sprite, SpriteList, Vec2

from src.visual import VData
from src.visual.vatlas import VAtlas, VTile


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
        force_first: bool = False,
    ) -> None:

        # ############################### PICK TEXTURE ####
        def pick_texture(who: str) -> VTile:
            if force_first:
                return self.atlas.textures[who][0]

            tile = [t for t in self.atlas.textures[who]]
            weights = [w.probability / 100 for w in self.atlas.textures[who]]

            return random.choices(tile, weights, k=1)[0]

        # ####################################
        tile = pick_texture(texture_name)
        if tile.no_rotation:
            angle = 0

        if isinstance(tile.texture, arcade.TextureAnimation):
            sprite = arcade.TextureAnimationSprite(
                animation=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=scale,
            )
            sprite.angle = angle
        else:
            sprite = arcade.Sprite(
                path_or_texture=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=scale,
                angle=angle,
            )

        self.sprites.append(sprite)

    # ########################################################################
    # ############################################################# SCALE ####
    # TODO: FIND A WAY TO ADPAT SPRITE SCALE !!!!!!!!!!!!!!!!!!!!!!!
    # TODO: FIND A WAY TO ADPAT SPRITE SCALE !!!!!!!!!!!!!!!!!!!!!!!
    # TODO: FIND A WAY TO ADPAT SPRITE SCALE !!!!!!!!!!!!!!!!!!!!!!!
    def _get_scale(self, size: int) -> float:
        return VData.SPRITE_SIZE / size

    # ########################################################################
    # ############################################################# CLEAR ####
    def clear(self) -> None:
        self.sprites.clear()

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update_animation(self, delta_time) -> None:
        self.sprites.update_animation(delta_time)
