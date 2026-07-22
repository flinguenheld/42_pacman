from arcade import Vec2

from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel
from src.visual.gui.ginput import GInput
from src.visual.gui.gwindow import GWindow
from src.visual.gui.gmenu_entry import GMenuEntry
from src.visual.gui.titles.gtitle_game_over import GTitleGameOver


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░░█░█░▀▄▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░▀░▀░░
class VGameOver(GWindow):
    def __init__(self, atlas: VAtlas, score: int = 42) -> None:
        super().__init__(
            atlas,
            title=GTitleGameOver(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=24,
                nb_cols=33,
                bevels=True,
                separators=[7, 17],
            ),
        )
        self.score = score

        # Score #############################
        self.text_score = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            font_size_factor=1.7,
            text=f"You loose with\n{score} points !",
            multiline=True,
            offset=Vec2(0, 250),
        )

        # Request ##########################
        self.text_request = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="Enter your name:",
            offset=Vec2(0, 90),
        )

        # Input ############################
        self.input = GInput(
            atlas=self.atlas,
            frame=self.frame,
            offset=Vec2(0, -40),
        )

        # Menu #############################
        self.menu = GMenu(
            atlas=self.atlas,
            choices={
                "SAVE": GMenuEntry.ToCall(
                    func=self.Process_input,
                    args=[],
                    # func=self.window.switch_view,
                    # args=[VNames.VIEW_WELCOME],
                ),
                "QUIT": GMenuEntry.ToCall(
                    func=self.window.switch_view,
                    args=[VNames.VIEW_WELCOME],
                ),
            },
            center_top_first=Vec2(self.frame.center_position.x, 140),
        )

        # --
        self.to_draw_and_update.append(self.menu)
        self.to_draw_and_update.append(self.input)
        self.to_draw_and_update.append(self.text_score)
        self.to_draw_and_update.append(self.text_request)

    # ########################################################################
    # ##################################################### PROCESS INPUT ####
    def Process_input(self) -> None:

        user_value = self.input.text.strip()

        if not user_value:
            self.input.toggle_help()
        else:
            # TODO: ADD HIGHSCORES MANAGEMENT HERE
            # TODO: ADD HIGHSCORES MANAGEMENT HERE
            # TODO: ADD HIGHSCORES MANAGEMENT HERE
            self.window.switch_view(VNames.VIEW_WELCOME)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.input.key_press_management(symbol, modifiers)
        self.menu.key_press(symbol)
