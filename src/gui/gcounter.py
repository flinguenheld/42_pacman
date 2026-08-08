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
    Each change launches the callback function.
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
    # ######################################################### KEY PRESS ####
    def on_key_press(self, symbol: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.count += 1
                self._update_text()
                self.run_callback()
            case arcade.key.LEFT:
                self.count -= 1
                self._update_text()
                self.run_callback()
            case _:
                pass
