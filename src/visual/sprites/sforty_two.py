from __future__ import annotations

import random
import arcade
from arcade import Vec2
from src.visual import VData
from src.visual.sprites.sprites import Sprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█▀█░█▀▄░▀█▀░█░█░░░▀█▀░█░█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█░█░█▀▄░░█░░░█░░░░░█░░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀▀▀░▀░▀░░▀░░░▀░░░░░▀░░▀░▀░▀▀▀░░
class SFortyTwo(Sprites):
    def __init__(self) -> None:
        super().__init__(file_basename="fortytwo")

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, data: set[Vec2]) -> None:

        # --
        self.reload_info()
        for point in data:
            file_name = random.choice(self._list_files(self.file_basename))
            path_sprite = f"{self.path}/{file_name}"

            self.sprites.append(
                arcade.Sprite(
                    path_or_texture=path_sprite,
                    scale=self.scale,
                    center_x=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.x,
                    center_y=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.y,
                )
            )
