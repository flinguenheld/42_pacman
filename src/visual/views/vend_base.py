from arcade import Vec2

from src.visual.gui.gbasic_button import GBasicButton
from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel
from src.visual.gui.ginput import GInput
from src.visual.gui.gwindow import GWindow
from src.visual.gui.titles.gtitle import GTitle
from src.high_scores.high_scores import HighScores


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▀▄░░░█▀▄░█▀█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░█░█░░░█▀▄░█▀█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀▀░░░░▀▀░░▀░▀░▀▀▀░▀▀▀░░
class VEndBase(GWindow):
    """
    Common base for victory and game over.
    Allow user to enter his name and save the score.
    """

    def __init__(
        self,
        atlas: VAtlas,
        title: GTitle,
        text: str,
        score: int,
    ) -> None:
        super().__init__(
            atlas,
            title=title,
            frame=GFrame(
                atlas=atlas,
                nb_rows=26,
                nb_cols=36,
                bevels=True,
                separators=[r for r in range(8, 19)],
            ),
        )
        self.score = score

        # Score #############################
        self.text_score = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            font_size_factor=1.7,
            text=text,
            multiline=True,
            offset=Vec2(0, 290),
        )

        # Request ##########################
        self.text_request = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="Enter your name:",
            offset=Vec2(0, 90),
            color=self.atlas.get_color("high_scores"),
        )

        # Input ############################
        self.input = GInput(
            atlas=self.atlas,
            frame=self.frame,
            offset=Vec2(0, -60),
            color=self.atlas.get_color("high_scores"),
        )

        # Menu #############################
        self.menu = GMenu(
            atlas=self.atlas,
            widgets=[
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=self.process_input,
                    text="SAVE",
                ),
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=lambda: self.window.switch_view(
                        VNames.VIEW_WELCOME
                    ),
                    text="QUIT",
                ),
            ],
            center_top_first=Vec2(self.frame.center_position.x, 150),
        )

        # --
        self.to_draw_and_update.append(self.menu)
        self.to_draw_and_update.append(self.input)
        self.to_draw_and_update.append(self.text_score)
        self.to_draw_and_update.append(self.text_request)

    # ########################################################################
    # ##################################################### PROCESS INPUT ####
    def process_input(self) -> None:

        user_value = self.input.text.strip()

        if not user_value:
            self.input.toggle_help()
        else:
            high_scores = HighScores()
            high_scores.save(user_value, self.score)
            self.window.switch_view(VNames.VIEW_WELCOME)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.input.on_key_press(symbol, modifiers)
        self.menu.on_key_press(symbol)
