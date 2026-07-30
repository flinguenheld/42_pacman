from arcade import Vec2

from src.visual.gui.gbasic_button import GBasicButton
from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.glabel import GLabel
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwindow import GWindow
from src.visual.gui.titles.gtitle_instructions import GTitleInstructions


# ░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀█░█▀▀░▀█▀░█▀▄░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░█░█░▀▀█░░█░░█▀▄░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class VIinstructions(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitleInstructions(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=35,
                nb_cols=43,
                bevels=True,
            ),
        )

        # --
        self.menu = GMenu(
            atlas=self.atlas,
            widgets=[
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=lambda: self.window.switch_view(
                        VNames.VIEW_PREVIOUS
                    ),
                    text="OK",
                ),
            ],
            center_top_first=Vec2(self.frame.center_position.x, 100),
        )

        self.to_draw_and_update.append(self.menu)

        # --
        self.text = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text=self.instructions(),
        )

        self.to_draw_and_update.append(self.text)

    # ########################################################################
    # ############################################################# SETUP ####
    def instructions(self) -> str:

        txt = "blah blah blah"

        return txt

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.on_key_press(symbol)
