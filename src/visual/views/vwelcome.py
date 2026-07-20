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
                nb_cols=25,
                separators=[480],
            ),
        )

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:

        self.menu = GMenu(
            self.atlas,
            {
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
            Vec2(400, 700),
        )

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        super().on_draw()
        with self.camera.activate():
            self.menu.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        super().on_update(delta_time)
        self.menu.update(delta_time)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
