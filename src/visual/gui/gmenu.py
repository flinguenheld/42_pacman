import arcade
from arcade import Vec2

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
        choices: dict[str, GMenuEntry.ToCall],
        center_top_first: Vec2,
    ) -> None:
        self.atlas = atlas

        self.choices = []
        for to_print, to_call in choices.items():
            new_entry = GMenuEntry(
                self.atlas,
                to_print,
                to_call,
                center=center_top_first,
            )

            center_top_first -= Vec2(
                0, atlas.font_size * GMenuEntry.FONT_SIZE_FACTOR * 1.5
            )
            self.choices.append(new_entry)

        self.current = 1
        self.next_up()

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        for choice in self.choices:
            choice.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        for choice in self.choices:
            choice.update(delta_time)

    # ########################################################################
    # ####################################################### KEY PRESSED ####
    def key_press(self, symbol: int) -> None:
        match symbol:
            case arcade.key.UP | arcade.key.Z | arcade.key.W | arcade.key.L:
                self.next_up()
            case arcade.key.DOWN | arcade.key.S | arcade.key.K:
                self.next_down()
            case arcade.key.ENTER | arcade.key.NUM_ENTER:
                self.choices[self.current].call_action()

    # ########################################################################
    # ######################################################### UP / DOWN ####
    def next_up(self) -> None:
        self.choices[self.current].active = False
        self.current = (self.current - 1) % len(self.choices)
        self.choices[self.current].active = True

    def next_down(self) -> None:
        self.choices[self.current].active = False
        self.current = (self.current + 1) % len(self.choices)
        self.choices[self.current].active = True
