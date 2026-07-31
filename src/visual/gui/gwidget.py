from abc import ABC
from typing import Any

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
