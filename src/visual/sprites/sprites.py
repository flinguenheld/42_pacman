from __future__ import annotations
import time

import os
import re
import arcade
import random
from enum import Enum
from typing import Any
from json import load as json_load
from arcade import SpriteList, Vec2

from src.visual import VData


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class Sprites:
    class Style(Enum):
        Fantasy = "fantasy"
        Medieval = "medieval"
        Scifi = "scifi"
        Tank = "tank"
        Test = "pirate"

    def __init__(self, folder: str) -> None:
        self.sprites: SpriteList = SpriteList()
        self.style = Sprites.Style.Test
        self.info: dict[str, Any] = {}
        self.folder = folder
        self.scale = 1.0
        self.path = ""

    # ########################################################################
    # ######################################################## NEXT STYLE ####
    def next_style(self) -> None:
        match self.style:
            case Sprites.Style.Fantasy:
                self.style = Sprites.Style.Medieval
            case Sprites.Style.Medieval:
                self.style = Sprites.Style.Scifi
            case Sprites.Style.Scifi:
                self.style = Sprites.Style.Tank

            case _:
                self.style = Sprites.Style.Fantasy

    # ########################################################################
    # ####################################################### RELOAD DATA ####
    def reload_info(self) -> None:
        # TODO keep info ??
        self.path = f"{VData.SPRITES}/maze/{self.style.value}"
        self.info = self._open_info(self.path)
        self.scale = self._get_scale(self.info["size"])
        self.path = f"{self.path}/{self.folder}"
        self.sprites.clear()
        random.seed(time.time())

    # ########################################################################
    # #################################################### ADD SUB SPRITE ####
    def add_sprite(self, center: Vec2, filename: str, angle: int = 0) -> None:
        def to_real_coordinate(point: Vec2) -> Vec2:
            return Vec2(
                VData.SPRITE_SHIFT + point.x * VData.SPRITE_SIZE,
                VData.SPRITE_SHIFT + point.y * VData.SPRITE_SIZE,
            )

        # file_name = random.choice(self._list_allowed_files(filename))

        file_name = self._randomly_pick(
            self._list_allowed_files(filename), self.info["more_probable"]
        )

        path_sprite = f"{self.path}/{file_name}"
        real_point = to_real_coordinate(center)

        # self.sprites.append(
        #     arcade.Sprite(
        #         path_or_texture=path_sprite,
        #         scale=self._get_scale(self.info["size"]),
        #         center_x=real_point.x,
        #         center_y=real_point.y,
        #     )
        # )

        if file_name in self.info["no_rotation"]:
            angle = 0

        sprite = arcade.Sprite(
            path_or_texture=path_sprite,
            scale=self._get_scale(self.info["size"]),
            # scale=-abs(self._get_scale(self.info["size"])),
            center_x=real_point.x,
            center_y=real_point.y,
            angle=angle,
        )
        # blah = sprite.texture.flip_horizontally()
        self.sprites.append(sprite)

    # ########################################################################
    # ####################################################### SPRITE INFO ####
    def _open_info(self, path: str) -> dict[str, Any]:
        try:
            with open(f"{path}/info.json", "r") as file:
                info: dict[str, Any] = json_load(file)
                return info
        except OSError:
            raise FileNotFoundError(f"info.json not found in {path}")

    # ########################################################################
    # ######################################################## LIST FILES ####

    # TODO: CLEAN THAT --------------------------------
    # TODO: CLEAN THAT --------------------------------
    # TODO: CLEAN THAT --------------------------------

    def _list_allowed_files(self, start: str) -> list[str]:
        # print(f"Get these files: {start}")
        reg = re.compile(f"""^{start}\d?\.png$""")
        return [file for file in os.listdir(self.path) if reg.match(file)]

    # ########################################################################
    # ##################################################### RANDOMLY PICK ####
    def _randomly_pick(self, choices: list[str], more_prob: list[str]) -> str:

        mp = next((c for c in choices if c in more_prob), None)

        if mp:
            if random.randint(0, 10) < 7:
                return mp

        return random.choice(choices)

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int) -> float:
        return VData.SPRITE_SIZE / size
