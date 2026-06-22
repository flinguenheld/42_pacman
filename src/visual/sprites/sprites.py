from __future__ import annotations

import os
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

    def __init__(self, file_basename: str) -> None:
        self.sprites: SpriteList = SpriteList()
        self.style = Sprites.Style.Medieval
        self.info: dict[str, Any] = {}
        self.scale = 1.0
        self.path = ""
        self.file_basename = file_basename

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
        self.path = f"{VData.SPRITES}/maze/{self.style.value}"
        self.info = self._open_info(self.path)
        self.scale = self._get_scale(self.info["size"])
        self.sprites.clear()

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, data: dict[Vec2, str] | set[Vec2]) -> None:

        if not isinstance(data, set):
            raise ValueError("Sprite only accepts a set as data.")

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
    def _list_files(self, start: str) -> list[str]:
        return [f for f in os.listdir(self.path) if f.startswith(start)]

    # ########################################################################
    # ############################################################# SCALE ####
    # TODO: Find a good way to deal with scale & size
    def _get_scale(self, size: int) -> float:
        match size:
            case 128:
                return 0.25
            case 64:
                return 0.5
            case 32:
                return 1.0
            case 16:
                return 2
            case _:
                return 1.0
