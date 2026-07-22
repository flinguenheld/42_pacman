import arcade
from mazegenerator import MazeGenerator

from src.visual.vgame import VGame
from src.visual.vatlas import VAtlas
from src.visual.vdata import VNames, VData
from src.visual.views.vpause import VPause
from src.visual.views.vwelcome import VWelcome
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
        self.vwelcome = VWelcome(self.atlas)
        self.previous_view: arcade.View = self.vwelcome

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.show_view(self.vwelcome)

    # ########################################################################
    # ####################################################### SWITCH VIEW ####
    def switch_view(self, to: VNames) -> None:

        def save_and_show(which: arcade.View) -> None:
            if self.current_view:
                self.previous_view = self.current_view
            self.show_view(which)

        match to:
            case VNames.VIEW_GAME:
                save_and_show(self.vgame)
            case VNames.VIEW_INSTRUCTIONS:
                save_and_show(VIinstructions(self.atlas))
            case VNames.VIEW_PAUSE:
                save_and_show(VPause(self.atlas))
            case VNames.VIEW_PREVIOUS:
                save_and_show(self.previous_view)
            case VNames.VIEW_WELCOME:
                save_and_show(self.vwelcome)

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        VData.width = width
        VData.height = height
