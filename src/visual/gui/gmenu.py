from src.visual.gui.gframe import GFrame
from typing import Any, Tuple
import arcade
from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.gui.gwidget import GWidget
from src.visual.gui.gmenu_entry import GMenuEntry


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class GMenu(GWidget):
    """
    Manage a simple menu which displays texts and manage the keyboard actions.
    Give a dict of GMenuEntry.ToCall and the position of the text on the top.
    """

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        widgets: list[Tuple[Any, dict[str, Any]]],
        center_top_first: Vec2,
    ) -> None:
        super().__init__(atlas, frame)

        self.entries: list[GMenuEntry] = []

        for class_type, kwargs in widgets:
            new_entry = GMenuEntry(
                atlas=self.atlas,
                frame=frame,
                button_class=class_type,
                kwargs=kwargs,
                offset_from_center_frame=center_top_first,
            )

            center_top_first -= Vec2(
                0, atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR * 1.6
            )
            self.entries.append(new_entry)

        self.current = 0
        self.entries[self.current].toggle_hoover()

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        for choice in self.entries:
            choice.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        for choice in self.entries:
            choice.update(delta_time)

    # ########################################################################
    # ####################################################### KEY PRESSED ####
    def key_press(self, symbol: int) -> None:
        match symbol:
            case arcade.key.UP:
                self.next_up()
            case arcade.key.DOWN:
                self.next_down()

        self.entries[self.current].on_key_press(symbol)

    # ########################################################################
    # ######################################################### UP / DOWN ####
    def next_up(self) -> None:
        self.entries[self.current].toggle_hoover()
        self.current = (self.current - 1) % len(self.entries)
        self.entries[self.current].toggle_hoover()

    def next_down(self) -> None:
        self.entries[self.current].toggle_hoover()
        self.current = (self.current + 1) % len(self.entries)
        self.entries[self.current].toggle_hoover()
