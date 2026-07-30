from arcade import Vec2

from src.visual.gui.gbasic_button import GBasicButton
from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwindow import GWindow
from src.visual.gui.titles.gtitle_pause import GTitlePause


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀█░█░█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█▀█░█░█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░
class VPause(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitlePause(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=14,
                nb_cols=24,
                bevels=True,
            ),
        )

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:

        self.menu = GMenu(
            atlas=self.atlas,
            widgets=[
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=lambda: self.window.switch_view(
                        VNames.VIEW_GAME_RESUME
                    ),
                    text="RESUME",
                ),
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=lambda: self.window.switch_view(
                        VNames.VIEW_INSTRUCTIONS
                    ),
                    text="INSTRUCTIONS",
                ),
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=lambda: self.window.switch_view(
                        VNames.VIEW_WELCOME
                    ),
                    text="GIVE UP",
                ),
            ],
            center_top_first=Vec2(self.frame.center_position.x, 280),
        )

        self.to_draw_and_update.append(self.menu)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.on_key_press(symbol)
