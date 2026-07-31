from collections.abc import Callable
import inspect
from typing import Any

from arcade import Vec2
import arcade

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel


class GButton(GLabel):
    type Callback = Callable[[], None] | Callable[[GLabel], None]

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: "Callback",
        offset: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.7,
        text: str = "",
        align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
        multiline: bool = False,
        width: int | None = None,
    ) -> None:
        super().__init__(
            atlas=atlas,
            frame=frame,
            offset=offset,
            font_size_factor=font_size_factor,
            text=text,
            color=arcade.color.WHITE,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            multiline=multiline,
            width=width,
        )
        self.update_color()
        self.callback = callback

    # TODO: Check if we even need the argument in the callback
    # If not, then we can just define Callback as "Callable[[], None]"
    # and simplify things a lot
    def run_callback(self) -> None:
        callback: Any = self.callback
        sig = inspect.signature(callback)
        if len(sig.parameters) == 0:
            callback()
        else:
            callback(self)

    def update_color(self) -> None:
        if self.active:
            self.text.color = self.atlas.get_color("menu_font_active")
        else:
            self.text.color = self.atlas.get_color("menu_font")

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
        self.update_color()
