import arcade
from arcade import Vec2

from src.gui.gmenu import GMenu
from src.data.enums import VNames
from src.gui.gframe import GFrame
from src.gui.glabel import GLabel
from src.gui.gbutton import GButton
from src.gui.gwindow import GWindow
from src.sprites.vatlas import VAtlas
from src.high_scores.high_scores import HighScores
from src.gui.titles.gtitle_pacman import GTitlePacman


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
            frame=self.frame,
            widgets=[
                (
                    GButton,
                    {
                        "text": "PLAY",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_NEW_GAME
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
                        "text": "EXIT",
                        "callback": arcade.exit,
                    },
                ),
            ],
            y_first_entry_from_frame_center=380,
        )

        # Scores ####################
        self.text_highscores_title = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            font_size_factor=1.3,
            text="High scores",
            offset_from_center_frame=Vec2(0, 120),
            color=self.atlas.get_color("high_scores"),
        )
        self.text_highscores = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text=str(HighScores()),
            multiline=True,
            offset_from_center_frame=Vec2(0, -170),
            color=self.atlas.get_color("high_scores"),
        )

        self.to_draw_update_press_release.extend(
            [self.menu, self.text_highscores_title, self.text_highscores]
        )
