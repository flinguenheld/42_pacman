from __future__ import annotations

import os
import re
import arcade
import random
from enum import Enum
from typing import Any
from json import load as json_load
from arcade import Sprite, SpriteList, Vec2

from src.utils.maze_grid_to_world_coords import maze_grid_to_world_coords
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
        Test = "test"

    def __init__(self, folder: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList()
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

    # ########################################################################
    # #################################################### ADD SUB SPRITE ####
    def add_sprite(self, center: Vec2, filename: str) -> None:
        file_name = random.choice(self._list_allowed_files(filename))
        path_sprite = f"{self.path}/{file_name}"
        real_point = maze_grid_to_world_coords(center)

        self.sprites.append(
            arcade.Sprite(
                path_or_texture=path_sprite,
                scale=self._get_scale(self.info["size"]),
                center_x=real_point.x,
                center_y=real_point.y,
            )
        )

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
    def _list_allowed_files(self, start: str) -> list[str]:
        reg = re.compile(f"""^{start}\d?\.png$""")
        return [file for file in os.listdir(self.path) if reg.match(file)]

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int) -> float:
        return VData.SPRITE_SIZE / size
