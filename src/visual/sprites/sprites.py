from __future__ import annotations

from enum import Enum
from typing import Any
from arcade import SpriteList, Vec2
from json import load as json_load

from src.visual import VData


class Sprites:
    class Style(Enum):
        Basic = "basic"
        Tree = "tree"
        PixelWater = "pixel_water"
        Fantasy = "fantasy"

    def __init__(self) -> None:
        self.sprites: SpriteList = SpriteList()
        self.style = Sprites.Style.Basic
        self.info = {}
        self.scale = 1
        self.path = ""

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, data: dict[Vec2, str] | set[Vec2]) -> None:
        self.path = f"{VData.SPRITES}/maze/{self.style.value}"
        self.info = self._open_info(self.path)
        self.scale = self._get_scale(self.info["size"])

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
