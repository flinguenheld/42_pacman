from __future__ import annotations
import random

import arcade
from arcade import Vec2

from src.visual import VData
from src.visual.sprites.sprites import Sprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▄█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class SWall(Sprites):
    def __init__(self) -> None:
        super().__init__()

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, data: dict[Vec2, str] | set[Vec2]) -> None:
        super().reload(data)

        if not isinstance(data, dict):
            raise ValueError("SWall only accepts a dictionary as data.")

        # --
        self.sprites.clear()
        for point, value in data.items():
            if self.info["wall"]["from_list"]:
                file_name = random.choice(self.info["wall"]["files"])
                path_sprite = f"{self.path}/{file_name}.png"
            else:
                path_sprite = f"{self.path}/{value}.png"

            self.sprites.append(
                arcade.Sprite(
                    path_or_texture=path_sprite,
                    scale=self.scale,
                    center_x=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.x,
                    center_y=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.y,
                )
            )
