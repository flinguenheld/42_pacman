from __future__ import annotations

import os
import re
import time
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
        Pirate = "pirate"

    def __init__(self, folder: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList()
        self.style = Sprites.Style.Pirate
        self.info: dict[str, Any] = {}
        self.folder = folder
        self.scale = 1.0
        self.path = ""

    # ########################################################################
    # ######################################################## NEXT STYLE ####
    def next_style(self) -> None:

        self.style = Sprites.Style.Pirate

        # match self.style:
        #     case Sprites.Style.Test:
        # case Sprites.Style.Fantasy:
        #     self.style = Sprites.Style.Medieval
        # case _:
        #     self.style = Sprites.Style.Fantasy

    # ########################################################################
    # ####################################################### RELOAD INFO ####
    def reload_info(self) -> None:
        random.seed(time.time())
        self.path = f"{VData.SPRITES}/maze/{self.style.value}"
        self.info = self._open_info_file(self.path)
        self.scale = self._get_scale(self.info["size"])
        self.path = f"{self.path}/{self.folder}"
        self.sprites.clear()

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def add_sprite(self, center: Vec2, filename: str, angle: int = 0) -> None:
        file_name = self._get_file(filename, self.info["more_probable"])
        path_sprite = f"{self.path}/{file_name}"
        real_point = maze_grid_to_world_coords(center)

        if file_name in self.info["no_rotation"]:
            angle = 0

        self.sprites.append(
            arcade.Sprite(
                path_or_texture=path_sprite,
                scale=self._get_scale(self.info["size"]),
                center_x=real_point.x,
                center_y=real_point.y,
                angle=angle,
            )
        )

    # ########################################################################
    # ####################################################### SPRITE INFO ####
    def _open_info_file(self, path: str) -> dict[str, Any]:
        try:
            with open(f"{path}/info.json", "r") as file:
                info: dict[str, Any] = json_load(file)
                return info
        except OSError:
            raise FileNotFoundError(f"info.json not found in {path}")

    # ########################################################################
    # ########################################################## GET FILE ####
    def _get_file(self, filename: str, more_probables: list[str]) -> str:
        """List all files in the current path which are named with a number
        filename1, filename2 ...
        Then randomly select one.
        Apply a bias if a file is in the more_probables list."""

        def list_allowed_files(start: str) -> list[str]:
            reg = re.compile(f"""^{start}\d?\.png$""")  # noqa: W605
            return [file for file in os.listdir(self.path) if reg.match(file)]

        def randomly_pick(choices: list[str]) -> str:
            more_prob = next((c for c in choices if c in more_probables), None)
            if more_prob and random.randint(0, 10) < 7:
                return more_prob
            return random.choice(choices)

        # --
        files = list_allowed_files(filename)
        return randomly_pick(files)

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int) -> float:
        return VData.SPRITE_SIZE / size
