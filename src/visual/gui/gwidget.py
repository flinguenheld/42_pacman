from typing import Any

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░▀█▀░█▀▄░█▀▀░█▀▀░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░░█░░█░█░█░█░█▀▀░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░▀░░░
class GWidget:
    """
    Base class for widgets.
    Contains a "elements" list to fill in children to automatically
    draw/update elements.
    """

    def __init__(self, atlas: VAtlas, frame: GFrame) -> None:
        self.atlas = atlas
        self.frame = frame
        self.elements: list[Any] = []

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float) -> None:
        for element in self.elements:
            if hasattr(element, "update"):
                element.update(delta_time)
            if hasattr(element, "update_animation"):
                element.update_animation(delta_time)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        for element in self.elements:
            if hasattr(element, "draw"):
                element.draw()
