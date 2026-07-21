import arcade
from arcade import Vec2

from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwindow import GWindow
from src.visual.gui.gmenu_entry import GMenuEntry
from src.visual.gui.title.gtitle_pacman import GTitlePacman


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░░░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▄█░█▀▀░█░░░█░░░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class VWelcome(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitlePacman(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=20,
                nb_cols=30,
                separators=[8],
                bevels=True,
            ),
        )

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:

        self.menu = GMenu(
            atlas=self.atlas,
            choices={
                "PLAY": GMenuEntry.ToCall(
                    func=self.window.switch_view,
                    args=[VNames.VIEW_GAME],
                ),
                "INSTRUCTIONS": GMenuEntry.ToCall(
                    func=self.window.switch_view,
                    args=[VNames.VIEW_GAME],
                ),
                "EXIT": GMenuEntry.ToCall(
                    func=arcade.exit,
                    args=[],
                ),
            },
            center_top_first=Vec2(self.frame.center_position.x, 550),
        )

        self.to_draw_and_update.append(self.menu)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
