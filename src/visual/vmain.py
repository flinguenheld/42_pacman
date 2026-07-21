import arcade
from mazegenerator import MazeGenerator

from src.visual.vgame import VGame
from src.visual.vatlas import VAtlas
from src.visual.vdata import VNames, VData
from src.visual.views.vpause import VPause
from src.visual.views.vwelcome import VWelcome


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

        self.vwelcome = VWelcome(self.atlas)
        self.vgame = VGame(self.atlas)

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.show_view(self.vwelcome)

    # ########################################################################
    # ####################################################### SWITCH VIEW ####
    def switch_view(self, to: VNames) -> None:
        match to:
            case VNames.VIEW_WELCOME:
                self.show_view(self.vwelcome)
            case VNames.VIEW_GAME:
                self.show_view(self.vgame)
            case VNames.VIEW_PAUSE:
                self.show_view(VPause(self.atlas))

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        VData.width = width
        VData.height = height
