import arcade
from arcade import Vec2

from src.visual.gui.gwidget import GWidget
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
        widgets: list[GWidget],
        center_top_first: Vec2,
    ) -> None:
        self.atlas = atlas

        self.entries: list[GMenuEntry] = []
        for widget in widgets:
            new_entry = GMenuEntry(
                atlas,
                widget,
                center_top_first
            )

            center_top_first -= Vec2(
                0, atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR * 1.6
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
    def on_key_press(self, symbol: int) -> None:
        match symbol:
            case arcade.key.UP:
                self.next_up()
            case arcade.key.DOWN:
                self.next_down()
            case arcade.key.ENTER | arcade.key.NUM_ENTER:
                self.entries[self.current].run_callback()
            case _:
                pass

    # ########################################################################
    # ######################################################### UP / DOWN ####
    def next_up(self) -> None:
        self.entries[self.current].active = False
        self.current = (self.current - 1) % len(self.entries)
        self.entries[self.current].active = True

    def next_down(self) -> None:
        self.entries[self.current].active = False
        self.current = (self.current + 1) % len(self.entries)
        self.entries[self.current].active = True
