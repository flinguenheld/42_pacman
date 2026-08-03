from typing import Any, Tuple, Type
import arcade
from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.gbutton import GButton
from src.visual.gui.gwidget import GWidget
from src.visual.gui.gmenu_entry import GMenuEntry


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class GMenu(GWidget):
    """
    Manage a simple menu which displays texts and manage the keyboard actions.
    Give a dict of GMenuEntry.ToCall and the position of the text on the top.

    The menu position is set from the frame center.
    """

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        widgets: list[Tuple[Type[GButton], dict[str, Any]]],
        y_first_entry_from_frame_center: int | float,
    ) -> None:
        super().__init__(atlas, frame)

        self.entries: list[GMenuEntry] = []

        # Create and set button positions --
        for class_type, kwargs in widgets:
            new_entry = GMenuEntry(
                atlas=self.atlas,
                frame=frame,
                button_class=class_type,
                kwargs=kwargs,
                offset_from_frame_center=Vec2(
                    0, y_first_entry_from_frame_center
                ),
            )

            y_first_entry_from_frame_center -= (
                atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR * 1.6
            )

            self.entries.append(new_entry)
            self.elements.append(new_entry)  # Manage draw & update

        self.current = 0
        self.entries[self.current].toggle_hoover()

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
