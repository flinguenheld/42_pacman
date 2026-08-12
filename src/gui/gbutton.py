import arcade
import inspect
from arcade import Vec2
from arcade.types import Color
from typing import Any
from collections.abc import Callable

from src.gui.gframe import GFrame
from src.gui.glabel import GLabel
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█░█░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▄░█░█░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀░▀░░
class GButton(GLabel):
    type Callback[type] = Callable[[], None] | Callable[[type], None]

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: Callback[Any],
        offset_from_center_frame: Vec2 | None = None,
        font_size_factor: float = 1.7,
        text: str = "",
        color: Color | None = None,
    ) -> None:
        super().__init__(
            atlas=atlas,
            frame=frame,
            offset_from_center_frame=offset_from_center_frame,
            font_size_factor=font_size_factor,
            text=text,
            color=color,
        )

        self.callback = callback

    # ########################################################################
    # ###################################################### RUN CALLBACK ####
    def run_callback(self) -> None:
        # MAGIC --
        callback: Any = self.callback
        sig = inspect.signature(callback)
        if len(sig.parameters) == 0:
            callback()
        else:
            callback(self)

    # ########################################################################
    # ############################################ KEY PRESSED / RELEASED ####
    def key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in [
            arcade.key.ENTER,
            arcade.key.NUM_ENTER,
            arcade.key.SPACE,
        ]:
            self.run_callback()
