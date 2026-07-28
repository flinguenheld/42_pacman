from __future__ import annotations
import random

from typing import Callable, Any
from dataclasses import dataclass
from arcade import Vec2, Text, SpriteList
from src.visual.gamestate import GameState

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░░█▀▀░█▀█░▀█▀░█▀▄░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░░█▀▀░█░█░░█░░█▀▄░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░░▀░░▀░▀░░▀░░░
class GMenuEntry:
    """
    Manage an entry for GMenu.
    Toggle its active property to draw an icon and with a special color.
    Save a ToCall object to launch with call_action().
    """

    FONT_SIZE_FACTOR: float = 1.7

    @dataclass
    class ToCall:
        func: Callable
        args: list[Any]

    def __init__(
        self,
        atlas: VAtlas,
        to_print: str,
        to_call: ToCall,
        center: Vec2,
    ) -> None:

        self.atlas = atlas
        self.to_call = to_call
        self.is_on = False

        # Text --
        self.text = Text(
            text=to_print,
            x=center.x,
            y=center.y,
            font_name=self.atlas.font_name,
            font_size=self.atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR,
            align="center",
            anchor_x="center",
            anchor_y="center",
            color=atlas.get_color("menu_font"),
        )

        # Icons --
        shift = self.text.content_width / 2 + VData.SPRITE_SIZE

        # QUESTION: Is it clean ?
        possible_tiles = ["player"]
        for id in range(4):
            possible_tiles.append(f"enemy_{id}_{GameState.Mode.CHASING.value}")

        tile_name = random.choice(possible_tiles)

        self.icons: SpriteList = SpriteList()
        tile = self.atlas.pick_tile(f"{tile_name}_right")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(center.x - shift - 5, center.y - 5),
            )
        )

        tile = self.atlas.pick_tile(f"{tile_name}_left")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(center.x + shift, center.y - 5),
            )
        )

    # ########################################################################
    # ####################################################### CALL ACTION ####
    def call_action(self) -> None:
        self.to_call.func(*self.to_call.args)

    # ########################################################################
    # ##################################################### TOGGLE ACTIVE ####
    @property
    def active(self) -> bool:
        return self.is_on

    @active.setter
    def active(self, value: bool) -> None:
        if value:
            self.text.color = self.atlas.get_color("menu_font_active")
        else:
            self.text.color = self.atlas.get_color("menu_font")

        self.is_on = value

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.text.draw()

        if self.is_on:
            self.icons.draw(pixelated=True)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.icons.update_animation(delta_time)
