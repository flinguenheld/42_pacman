from abc import ABC

from arcade import Vec2

from src.visual.gui.gframe import GFrame
from src.visual.vatlas import VAtlas


class GWidget(ABC):
    def __init__(self, atlas: VAtlas, frame: GFrame) -> None:
        self.atlas = atlas
        self.frame = frame

        self._active = False

    def update(self, delta_time: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        pass

    def run_callback(self) -> None:
        pass

    @property
    def left(self) -> float:
        raise NotImplementedError(
            "Not implemented in GWidget, please implement in subclasses"
        )

    @property
    def right(self) -> float:
        raise NotImplementedError(
            "Not implemented in GWidget, please implement in subclasses"
        )

    def update_offset(self, offset: Vec2) -> None:
        raise NotImplementedError(
            "Not implemented in GWidget, please implement in subclasses"
        )

    @property
    def center(self) -> Vec2:
        raise NotImplementedError(
            "Not implemented in GWidget, please implement in subclasses"
        )

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
        self.update_color()

    def update_color(self) -> None:
        pass
