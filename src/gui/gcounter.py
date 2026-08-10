from __future__ import annotations

import arcade
from arcade import Vec2
from arcade.types import Color

from src.gui.gframe import GFrame
from src.gui.gbutton import GButton
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█▀█░█░█░█▀█░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█░█░█░█░█░█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
class GCounter(GButton):
    """
    A counter is a button which displays a number on its right.
    The value can be changed with arrows.
    Maintain the button to change values faster.
    Each button release launches the callback function.
    """

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: GButton.Callback[GCounter],
        text: str,
        color: Color,
        offset_from_center_frame: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.7,
        count: int = 0,
        min: int = 0,
    ) -> None:
        super().__init__(
            atlas=atlas,
            frame=frame,
            callback=callback,
            offset_from_center_frame=offset_from_center_frame,
            font_size_factor=font_size_factor,
            text=text,
            color=color,
        )

        # --
        self.min = min
        self.count = count
        self.base_text = text
        self._update_text()

        # --
        self.velocity: int = 0
        self.time_delta: float = 0.0
        self.time_pressed: float = 0.0

    # ########################################################################
    # #################################################### COUNT PROPERTY ####
    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        if value >= self.min:
            self._count = value

    # ########################################################################
    # ####################################################### UPDATE TEXT ####
    def _update_text(self) -> None:
        self.text = f"{self.base_text}:  {self.count}"

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:

        if self.velocity != 0:
            if self.time_pressed == 0:
                self.count += self.velocity
                self._update_text()

            elif self.time_pressed > 0.200 and self.time_delta > 0.008:
                self.count += self.velocity
                self._update_text()
                self.time_delta = 0

            self.time_delta += delta_time
            self.time_pressed += delta_time

    # ########################################################################
    # ######################################################### KEY PRESS ####
    def key_press(self, symbol: int, modifiers: int) -> None:
        self.time_pressed = 0.0
        match symbol:
            case arcade.key.RIGHT:
                self.velocity = 1
            case arcade.key.LEFT:
                self.velocity = -1
            case _:
                pass

    def key_release(self, symbol: int, modifiers: int) -> None:
        self.velocity = 0
        self.run_callback()
