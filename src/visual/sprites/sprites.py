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
    # ################################################### ANGLED FILENAME ####
    def get_angled_filename(self, point: Vec2, data: set[Vec2]) -> str:
        file_name = self.file_basename + "_"

        if Vec2(point.x, point.y - 1) in data:
            file_name += "B"
        if Vec2(point.x - 1, point.y) in data:
            file_name += "L"
        if Vec2(point.x + 1, point.y) in data:
            file_name += "R"
        if Vec2(point.x, point.y + 1) in data:
            file_name += "T"

        return file_name

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, data: set[Vec2]) -> None:

        self.reload_info()
        for point in data:
            if self.info[self.file_basename]["angles"]:
                file_name = self.get_angled_filename(point, data)
                path_sprite = f"{self.path}/{file_name}.png"
            else:
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
