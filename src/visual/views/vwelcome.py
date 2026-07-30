import arcade
from arcade import Vec2

from src.visual.gui.gbasic_button import GBasicButton
from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel
from src.visual.gui.gwindow import GWindow
from src.high_scores.high_scores import HighScores
from src.visual.gui.titles.gtitle_pacman import GTitlePacman


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
                nb_rows=29,
                nb_cols=35,
                separators=[s for s in range(9, 27)],
                bevels=True,
            ),
        )

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:

        # Menu ######################
        self.menu = GMenu(
            atlas=self.atlas,
            widgets=[
                GBasicButton(
                    atlas=self.atlas,
                    frame=self.frame,
                    callback=lambda: self.window.switch_view(
                        VNames.VIEW_GAME_NEW
                    ),
                    text="PLAY",
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
                    callback=arcade.exit,
                    text="EXIT",
                ),
            ],
            center_top_first=Vec2(0, 400),
        )

        # Scores ####################
        self.text_highscores_title = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            font_size_factor=1.3,
            text="High scores",
            offset=Vec2(0, 120),
            color=self.atlas.get_color("high_scores"),
        )
        self.text_highscores = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text=str(HighScores()),
            multiline=True,
            offset=Vec2(0, -170),
            color=self.atlas.get_color("high_scores"),
        )

        self.to_draw_and_update.append(self.menu)
        self.to_draw_and_update.append(self.text_highscores_title)
        self.to_draw_and_update.append(self.text_highscores)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.on_key_press(symbol)
