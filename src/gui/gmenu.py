import arcade
from typing import Any
from arcade import Vec2

from src.gui.gframe import GFrame
from src.gui.gbutton import GButton
from src.gui.gwidget import GWidget
from src.sprites.vatlas import VAtlas
from src.gui.gmenu_entry import GMenuEntry


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class GMenu(GWidget):
    """
    Manage a simple menu which displays texts and manage the keyboard actions.
    Give a dict of GMenuEntry.ToCall and the position of the text on the top.

    The menu position is set from the frame center.

    Use extra_line_spaces to add a padding at the given indexes.
    """

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        widgets: list[tuple[type[GButton], dict[str, Any]]],
        y_first_entry_from_frame_center: int | float,
        extra_line_spaces: list[int] = list(),
        escape_widget_index: int = -1,
    ) -> None:
        super().__init__(atlas, frame)
        self.escape_widget_index = escape_widget_index
        self.entries: list[GMenuEntry] = []

        # Create and set button positions --
        for i, (class_type, kwargs) in enumerate(widgets):
            new_entry = GMenuEntry(
                atlas=self.atlas,
                frame=frame,
                button_class=class_type,
                kwargs=kwargs,
                offset_from_frame_center=Vec2(
                    0, y_first_entry_from_frame_center
                ),
            )

            # Ligne space --
            if i in extra_line_spaces:
                space = atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR * 3
            else:
                space = atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR * 1.7
            y_first_entry_from_frame_center -= space

            # --
            self.entries.append(new_entry)
            self.elements.append(new_entry)  # Manage draw & update

        # --
        self.current = 0
        self.entries[self.current].toggle_hoover()

    # ########################################################################
    # ####################################################### KEY PRESSED ####
    def key_press(self, symbol: int) -> None:
        match symbol:
            case arcade.key.ESCAPE:
                self.entries[self.escape_widget_index].on_key_press(
                    arcade.key.ENTER
                )
            case arcade.key.UP:
                self.next_up()
            case arcade.key.DOWN:
                self.next_down()
            case _:
                pass

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
