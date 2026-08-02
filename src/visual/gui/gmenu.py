import arcade
from arcade import Vec2

from src.visual.gui.glabel import GLabel
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu_entry import GMenuEntry


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class GMenu:
    """
    Manage a simple menu which displays texts and manage the keyboard actions.
    Give a dict of GMenuEntry.ToCall and the position of the text on the top.
    """

    def __init__(
        self,
        atlas: VAtlas,
        widgets: list[GLabel],
        center_top_first: Vec2,
    ) -> None:
        self.atlas = atlas

        self.entries: list[GMenuEntry] = []
        for widget in widgets:
            new_entry = GMenuEntry(atlas, widget, center_top_first)

            center_top_first -= Vec2(
                0, atlas.font_size * widget.font_size_factor * 1.6
            )
            self.entries.append(new_entry)

        self.current = 0
        self.entries[self.current].active = True

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        for entry in self.entries:
            entry.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        for entry in self.entries:
            entry.update(delta_time)

    # ########################################################################
    # ####################################################### KEY PRESSED ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.UP:
                self.next_up()
            case arcade.key.DOWN:
                self.next_down()
            case _:
                pass
        self.entries[self.current].on_key_press(symbol, modifiers)

    # ########################################################################
    # ######################################################### UP / DOWN ####
    def next_up(self) -> None:
        self.entries[self.current].active = False

        self.current -= 1
        if self.current < 0:
            self.current = len(self.entries) - 1
        while (
            self.current > 0
            and not self.entries[self.current].widget.selectable
        ):
            self.current -= 1

        self.entries[self.current].active = True

    def next_down(self) -> None:
        self.entries[self.current].active = False

        self.current += 1
        if self.current >= len(self.entries):
            self.current = 0
        while (
            self.current < len(self.entries) - 1
            and not self.entries[self.current].widget.selectable
        ):
            self.current += 1

        self.entries[self.current].active = True
