from __future__ import annotations

import arcade
from enum import Enum
from typing import Any
from json import load as json_load
from arcade import SpriteList, Vec2

from src.visual import VData
from src.maze.maze_wrapper import Maze


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▄█░█▀█░█░░░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class SWall:
    class Style(Enum):
        Basic = "basic"
        Tree = "tree"
        Edges = "edges"
        Briks = "briks"
        Ice = "ice"
        SquareBriks = "square_briks"

    def __init__(self) -> None:
        self._sprite_list: SpriteList = SpriteList()

    @property
    def sprites(self) -> SpriteList:
        return self._sprite_list

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, seed: int, size: Vec2) -> None:
        self.maze_gen = Maze(seed, size)
        self.maze_gen.generate_new_maze()
        self.maze_gen.build_maze()

    # ########################################################################
    # ####################################################### SPRITE INFO ####
    def _open_info(self, path: str) -> dict[str, Any]:
        try:
            with open(f"{path}info.json", "r") as file:
                info: dict[str, Any] = json_load(file)
                return info
        except OSError:
            raise FileNotFoundError(f"info.json not found in {path}")

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
                return 1.5
            case _:
                return 1.0

    # ########################################################################
    # ###################################################### CHANGE STYLE ####
    def change_style(self, style: SWall.Style) -> None:

        path = f"{VData.SPRITES}wall/{style.value}/"
        info = self._open_info(path)
        scale = self._get_scale(info["size"])

        for point, value in self.maze_gen.maze.items():
            if info["unique"]:
                path_sprite = f"{path}{style.value}.png"
            else:
                path_sprite = f"{path}{style.value}_{value}.png"

            self._sprite_list.append(
                arcade.Sprite(
                    path_or_texture=path_sprite,
                    scale=scale,
                    center_x=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.x,
                    center_y=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.y,
                )
            )
