import arcade
import random
from typing import Any
from arcade import Sprite, SpriteList, Vec2

from src.visual import VData
from src.maze.maze_wrapper import Maze
from src.visual.vatlas import VAtlas, VTile


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class Sprites:
    def __init__(self, atlas: VAtlas, base_name: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList(use_spatial_hash=True)
        self.base_name: str = base_name
        self.info: dict[str, Any] = {}
        self.atlas = atlas

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def add_sprite(
        self,
        texture_name: str,
        center: Vec2,
        force_first_texture: bool = False,
        background: bool = False,
    ) -> None:
        # ############################### PICK TEXTURE ####
        def pick_texture(who: str) -> VTile:
            if force_first_texture:
                return self.atlas.textures[who][0]

            tile = [t for t in self.atlas.textures[who]]
            weights = [w.probability / 100 for w in self.atlas.textures[who]]

            return random.choices(tile, weights, k=1)[0]

        # ####################################
        tile = pick_texture(texture_name)
        angle = random.choice(tile.allowed_angles)
        if not background:
            center = Maze.to_world_coords(center)

        if isinstance(tile.texture, arcade.TextureAnimation):
            sprite_animation: Sprite = arcade.TextureAnimationSprite(
                animation=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=self._get_scale(tile.width, background),
            )
            sprite_animation.angle = angle
            self.sprites.append(sprite_animation)
        else:
            self.sprites.append(
                arcade.Sprite(
                    path_or_texture=tile.texture,
                    center_x=center.x,
                    center_y=center.y,
                    scale=self._get_scale(tile.width, background),
                    angle=angle,
                )
            )

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int, background: bool = False) -> float:
        if background:
            return VData.SPRITE_SIZE_BACKGROUND / size
        return VData.SPRITE_SIZE / size

    # ########################################################################
    # ############################################################# CLEAR ####
    def clear(self) -> None:
        self.sprites.clear()

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update_animation(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)
