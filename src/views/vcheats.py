from src.gui.gmenu import GMenu
from src.data.vdata import VNames
from src.gui.gframe import GFrame
from src.gui.gwindow import GWindow
from src.gui.gbutton import GButton
from src.sprites.vatlas import VAtlas
from src.gui.gcounter import GCounter
from src.data.gamestate import GameState
from src.gui.gtoggle_button import GToggleButton
from src.gui.titles.gtitle_cheats import GTitleCheats


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█░█░█▀▀░█▀█░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░░░█▀█░█▀▀░█▀█░░█░░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░▀▀▀░░
class VCheats(GWindow):
    def __init__(self, atlas: VAtlas, gamestate: GameState) -> None:
        super().__init__(
            atlas,
            title=GTitleCheats(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=20,
                nb_cols=30,
                bevels=True,
                separators=[12],
            ),
        )
        self.gamestate = gamestate
        self.cheats = gamestate.cheats

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        # Menu ######################
        self.menu = GMenu(
            atlas=self.atlas,
            frame=self.frame,
            widgets=[
                (
                    GToggleButton,
                    {
                        "text": "GOD MODE",
                        "callback": lambda: self.cheats.toggle_god_mode(),
                        "pressed": self.gamestate.cheats.god_mode,
                    },
                ),
                (
                    GToggleButton,
                    {
                        "text": "NO CLIP",
                        "callback": lambda: self.cheats.toggle_no_clip(),
                        "pressed": self.gamestate.cheats.no_clip,
                    },
                ),
                (
                    GCounter,
                    {
                        "text": "LIVES",
                        "callback": lambda button: self.cheats.update_lives(
                            button.count
                        ),
                        "count": self.gamestate.lives,
                    },
                ),
                (
                    GCounter,
                    {
                        "text": "AMOUNT OF ENEMIES",
                        "callback": lambda button: (
                            self.cheats.update_amount_of_enemies(button.count)
                        ),
                        "count": self.gamestate.amount_of_enemies,
                    },
                ),
                (
                    GButton,
                    {
                        "text": "GO TO NEXT LEVEL",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_NEXT_LEVEL
                        ),
                    },
                ),
                (
                    GButton,
                    {
                        "text": "GO BACK",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_PREVIOUS
                        ),
                    },
                ),
            ],
            y_first_entry_from_frame_center=210,
            extra_line_spaces=[3],
        )

        self.to_draw_and_update.append(self.menu)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
