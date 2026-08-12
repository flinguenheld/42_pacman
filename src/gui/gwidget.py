from typing import Any

from src.gui.gframe import GFrame
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░▀█▀░█▀▄░█▀▀░█▀▀░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░░█░░█░█░█░█░█▀▀░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░▀░░░
class GWidget:
    """
    Base class for widgets.

    Contains a "to_draw_update_press_release" list to fill in children
    to automatically manage elements.
    It will call objects which contain
    draw/update/key_press/key_release methods.
    """

    def __init__(self, atlas: VAtlas, frame: GFrame) -> None:
        self.atlas = atlas
        self.frame = frame

        self.to_draw_update_press_release: list[Any] = []

    # ########################################################################
    # ################################################## ON DRAW / UPDATE ####
    def draw(self) -> None:
        for widget in self.to_draw_update_press_release:
            if hasattr(widget, "draw"):
                widget.draw()

    def update(self, delta_time: float) -> None:
        for widget in self.to_draw_update_press_release:
            if hasattr(widget, "update"):
                widget.update(delta_time)
            if hasattr(widget, "update_animation"):
                widget.update_animation(delta_time)

    # ########################################################################
    # ############################################ ON KEY PRESS / RELEASE ####
    def key_press(self, symbol: int, modifiers: int) -> None:
        for widget in self.to_draw_update_press_release:
            if hasattr(widget, "key_press"):
                widget.key_press(symbol, modifiers)

    def key_release(self, symbol: int, modifiers: int) -> None:
        for widget in self.to_draw_update_press_release:
            if hasattr(widget, "key_release"):
                widget.key_release(symbol, modifiers)
