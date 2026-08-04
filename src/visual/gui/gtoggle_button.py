from __future__ import annotations

import arcade
from arcade import Vec2
from arcade.types import Color

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.gbutton import GButton


# ░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█▀█░█▀▀░█▀▀░█░░░█▀▀░░░█▀▄░█░█░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░█░█░░█░░█░█░█░█░█░█░█░░░█▀▀░░░█▀▄░█░█░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀░▀░░
class GToggleButton(GButton):
    """
    A toggle button is a button that can be in one of two states:
       - pressed
       - not pressed

    The value can be changed with arrows.
    Each change launches the callback function.
    """

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: GButton.Callback[GToggleButton],
        text: str,
        pressed: bool = False,
        offset_from_center_frame: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.7,
        color: Color | None = None,
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
        self.pressed = pressed
        self.base_text = text
        self._update_text()

    # ########################################################################
    # ####################################################### UPDATE TEXT ####
    def _update_text(self) -> None:
        if self.pressed:
            self.text = f"{self.base_text}:  ON"
        else:
            self.text = f"{self.base_text}:  OFF"

    # ########################################################################
    # ######################################################### KEY PRESS ####
    def on_key_press(self, symbol: int) -> None:
        if symbol in [
            arcade.key.ENTER,
            arcade.key.NUM_ENTER,
            arcade.key.SPACE,
            # --
            arcade.key.LEFT,
            arcade.key.RIGHT,
        ]:
            self.pressed = not self.pressed
            self._update_text()
            self.run_callback()
