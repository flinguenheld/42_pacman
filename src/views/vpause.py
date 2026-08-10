from src.gui.gmenu import GMenu
from src.gui.gframe import GFrame
from src.data.vdata import VNames
from src.gui.gwindow import GWindow
from src.gui.gbutton import GButton
from src.sprites.vatlas import VAtlas
from src.gui.titles.gtitle_pause import GTitlePause


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
                nb_rows=15,
                nb_cols=24,
                bevels=True,
            ),
        )

        self.setup()
        self.to_draw_update_press_release.append(self.menu)

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:

        self.menu = GMenu(
            atlas=self.atlas,
            frame=self.frame,
            widgets=[
                (
                    GButton,
                    {
                        "text": "RESUME",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_GAME_RESUME
                        ),
                    },
                ),
                (
                    GButton,
                    {
                        "text": "INSTRUCTIONS",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_INSTRUCTIONS
                        ),
                    },
                ),
                (
                    GButton,
                    {
                        "text": "CHEATS",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_CHEATS,
                        ),
                    },
                ),
                (
                    GButton,
                    {
                        "text": "GIVE UP",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_WELCOME
                        ),
                    },
                ),
            ],
            y_first_entry_from_frame_center=110,
            escape_widget_index=0,
        )
