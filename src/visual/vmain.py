import arcade
from typing import Tuple
from mazegenerator import MazeGenerator

from src.visual.vgame import VGame
from src.visual.vatlas import VAtlas
from src.visual.vdata import VNames, VData
from src.visual.views.vpause import VPause
from src.visual.views.vvictory import VVictory
from src.visual.views.vwelcome import VWelcome
from src.visual.views.vgame_over import VGameOver
from src.visual.views.vinstructions import VIinstructions


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░█▀█░▀█▀░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░░█░░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░░
class VMain(arcade.Window):
    def __init__(self) -> None:
        super().__init__(
            VData.width,
            VData.height,
            "Pac-man",
            resizable=True,
        )

        self.maze_generator = MazeGenerator()
        self.maze_generator.generate()
        print(self.maze_generator.maze)

        arcade.resources.load_kenney_fonts()

        self.atlas = VAtlas()
        self.atlas.load()

        self.vgame = VGame(self.atlas)
        self.views_prev_curr: Tuple[VNames, VNames] = (
            VNames.VIEW_WELCOME,
            VNames.VIEW_WELCOME,
        )

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.switch_view(VNames.VIEW_WELCOME)
        # self.show_view(VGameOver(self.atlas))
        # self.show_view(VVictory(self.atlas))

    # ########################################################################
    # ####################################################### SWITCH VIEW ####
    def switch_view(self, to: VNames) -> None:

        def save_and_show(which: arcade.View) -> None:
            self.views_prev_curr = (self.views_prev_curr[1], to)
            self.show_view(which)

        match to:
            case VNames.VIEW_GAME:
                save_and_show(self.vgame)
            case VNames.VIEW_GAMEOVER:
                save_and_show(VGameOver(self.atlas))
            case VNames.VIEW_INSTRUCTIONS:
                save_and_show(VIinstructions(self.atlas))
            case VNames.VIEW_PAUSE:
                save_and_show(VPause(self.atlas))
            case VNames.VIEW_WELCOME:
                save_and_show(VWelcome(self.atlas))
            case VNames.VIEW_VICTORY:
                save_and_show(VVictory(self.atlas))

            case VNames.VIEW_PREVIOUS:
                self.switch_view(self.views_prev_curr[0])

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        VData.width = width
        VData.height = height
