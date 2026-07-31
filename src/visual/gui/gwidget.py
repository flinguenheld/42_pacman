from abc import ABC
from typing import Any

from arcade import Vec2

from src.visual.gui.gframe import GFrame
from src.visual.vatlas import VAtlas


class GWidget(ABC):
    def __init__(self, atlas: VAtlas, frame: GFrame) -> None:
        self.atlas = atlas
        self.frame = frame

        self._active = False

        self.elements: list[Any] = []

    # TODO: Not sure if this is better than just overriding these methods
    # in subclasses and manually calling draw and update on the elements.
    def update(self, delta_time: float) -> None:
        for element in self.elements:
            if hasattr(element, "update"):
                element.update(delta_time)
            if hasattr(element, "update_animation"):
                element.update_animation(delta_time)

    def draw(self) -> None:
        for element in self.elements:
            if hasattr(element, "draw"):
                element.draw()

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
