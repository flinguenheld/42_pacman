from arcade import Vec2

from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel
from src.visual.gui.gwindow import GWindow
from src.visual.gui.gmenu_entry import GMenuEntry
from src.visual.gui.titles.gtitle_game_over import GTitleGameOver


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░░█░█░▀▄▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░▀░▀░░
class VGameOver(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitleGameOver(atlas),
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
            choices={
                "CRY": GMenuEntry.ToCall(
                    func=self.window.switch_view,
                    args=[VNames.VIEW_WELCOME],
                ),
            },
            center_top_first=Vec2(self.frame.center_position.x, 100),
        )

        self.to_draw_and_update.append(self.menu)

        # --
        self.text = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text=self.final_score(),
        )

        self.to_draw_and_update.append(self.text)

    # ########################################################################
    # ############################################################# SETUP ####
    def final_score(self) -> str:

        txt = "blah blah blah"

        return txt

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
