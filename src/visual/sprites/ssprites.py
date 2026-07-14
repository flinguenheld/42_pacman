import random
from arcade import Sprite, SpriteList, Vec2

from src.visual.vdata import VData
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

        self.sprites.append(
            self.atlas.tile_to_sprite(
                tile=tile,
                center=center,
                angle=angle,
                sprite_size=sprite_size,
            )
        )

    # ########################################################################
    # ############################################################# CLEAR ####
    def clear(self) -> None:
        self.sprites.clear()

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update_animation(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)
