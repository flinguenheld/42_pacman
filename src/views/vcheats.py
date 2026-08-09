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
    def __init__(self, atlas: VAtlas, game_state: GameState) -> None:
        super().__init__(
            atlas,
            title=GTitleCheats(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=14,
                nb_cols=24,
                bevels=True,
            ),
        )
        self.game_state = game_state
        self.cheats = game_state.cheats

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
                        "pressed": self.game_state.cheats.god_mode,
                    },
                ),
                (
                    GCounter,
                    {
                        "text": "LIVES",
                        "callback": lambda button: self.cheats.update_lives(
                            button.count
                        ),
                        "count": self.game_state.lives,
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
            y_first_entry_from_frame_center=140,
            extra_line_spaces=[2],
        )

        self.to_draw_and_update.append(self.menu)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
