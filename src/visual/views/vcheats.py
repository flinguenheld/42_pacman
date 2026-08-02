from arcade import Vec2

from src.visual.gamestate import GameState
from src.visual.gui.gbutton import GButton
from src.visual.gui.gcounter import GCounter
from src.visual.gui.gpadding import GPadding
from src.visual.gui.gtogglebutton import GToggleButton
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwindow import GWindow
from src.visual.gui.titles.gtitle_pause import GTitlePause
from src.visual.vdata import VNames


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀█░█░█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█▀█░█░█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░
class VCheats(GWindow):
    def __init__(self, atlas: VAtlas, game_state: GameState) -> None:
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
        self.game_state = game_state
        self.cheats = game_state.cheats
        self.setup()

    def on_show_view(self) -> None:
        self.lives_counter.count = self.game_state.lives

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.god_mode_button = GToggleButton(
            atlas=self.atlas,
            frame=self.frame,
            # update the god_mode variable when the button is pressed
            callback=lambda: self.cheats.toggle_god_mode(),
            pressed=self.cheats.god_mode,
            text="GOD MODE",
            font_size_factor=1,
        )
        self.lives_counter = GCounter(
            atlas=self.atlas,
            frame=self.frame,
            update_callback=lambda button: self.cheats.update_lives(
                button.count
            ),
            count=self.game_state.lives,
            text="LIVES",
            font_size_factor=1,
        )
        self.back_button = GButton(
            atlas=self.atlas,
            frame=self.frame,
            callback=lambda: self.window.switch_view(VNames.VIEW_PREVIOUS),
            text="BACK",
        )

        self.menu = GMenu(
            atlas=self.atlas,
            widgets=[
                self.god_mode_button,
                self.lives_counter,
                GPadding(
                    atlas=self.atlas,
                    frame=self.frame,
                    padding=4.0,
                ),
                self.back_button,
            ],
            center_top_first=Vec2(0, 115),
        )

        self.to_draw_and_update.append(self.menu)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.on_key_press(symbol, modifiers)
