from __future__ import annotations

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

    # ########################################################################
    # #################################################### ADD SUB SPRITE ####
    def add_sub_sprite(self, center: Vec2, iner: Vec2, filename: str):
        def to_real_coordinate(point: Vec2) -> Vec2:
            return Vec2(
                VData.SPRITE_SHIFT + point.x * VData.SPRITE_SIZE * 2,
                VData.SPRITE_SHIFT + point.y * VData.SPRITE_SIZE * 2,
                # VData.SPRITE_SHIFT + point.x * VData.SPRITE_SIZE * 3,
                # VData.SPRITE_SHIFT + point.y * VData.SPRITE_SIZE * 3,
            )

        # Real coordinates --
        file_name = random.choice(self._list_files(filename))
        path_sprite = f"{self.path}/{file_name}"
        point = to_real_coordinate(center)
        point = Vec2(
            point.x + VData.SPRITE_SIZE * iner.x * 0.5,
            point.y + VData.SPRITE_SIZE * iner.y * 0.5,
        )

        self.sprites.append(
            arcade.Sprite(
                path_or_texture=path_sprite,
                # scale=0.25,
                scale=1,
                center_x=point.x,
                center_y=point.y,
            )
        )

    def reload(self, data: set[Vec2]) -> None:

        def strait(is_open: bool, iner: Vec2, txt: str):
            if is_open:
                self.add_sub_sprite(point, iner, "middle")
            else:
                self.add_sub_sprite(point, iner, txt)

        def angles(
            is_open_horizontal: bool,
            is_open_vertical: bool,
            is_open_angle: bool,
            iner: Vec2,
            txt_hor: str,
            txt_ver: str,
        ):
            match (is_open_horizontal, is_open_vertical):
                case False, False:
                    self.add_sub_sprite(point, iner, f"{txt_ver}_{txt_hor}")
                case False, True:
                    self.add_sub_sprite(point, iner, txt_hor)
                case True, False:
                    self.add_sub_sprite(point, iner, txt_ver)
                case True, True:
                    if is_open_angle:
                        self.add_sub_sprite(point, iner, "middle")
                    else:
                        self.add_sub_sprite(
                            point, iner, f"angle_{txt_ver}_{txt_hor}"
                        )

        # Basic coordinates --
        self.reload_info()
        for point in data:
            is_top = Vec2(point.x, point.y + 1) in data
            is_right = Vec2(point.x + 1, point.y) in data
            is_bot = Vec2(point.x, point.y - 1) in data
            is_left = Vec2(point.x - 1, point.y) in data

            is_top_left = Vec2(point.x - 1, point.y + 1) in data
            is_top_right = Vec2(point.x + 1, point.y + 1) in data
            is_bot_left = Vec2(point.x - 1, point.y - 1) in data
            is_bot_right = Vec2(point.x + 1, point.y - 1) in data

            self.add_sub_sprite(point, Vec2(0, 0), "middle")

            # strait(is_top, Vec2(0, 1), "top")
            # strait(is_bot, Vec2(0, -1), "bot")
            # strait(is_right, Vec2(1, 0), "right")
            # strait(is_left, Vec2(-1, 0), "left")

            angles(is_left, is_top, is_top_left, Vec2(-1, 1), "left", "top")
            angles(is_right, is_top, is_top_right, Vec2(1, 1), "right", "top")
            angles(is_right, is_bot, is_bot_right, Vec2(1, -1), "right", "bot")
            angles(is_left, is_bot, is_bot_left, Vec2(-1, -1), "left", "bot")

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
        reg = re.compile(f"""^{start}\d?\.png$""")
        return [file for file in os.listdir(self.path) if reg.match(file)]

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
