from src.visual.vatlas import VAtlas
import arcade
from src.visual.vgame import VGame
from src.visual.vmenu import VMenu
from src.visual.vpause import VPause
from mazegenerator import MazeGenerator
from src.visual.vdata import VNames, VData


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

        self.vmenu = VMenu(self.atlas)
        self.vgame = VGame(self.atlas)

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""
        # pass
        self.show_view(self.vmenu)

    # ########################################################################
    # ####################################################### SWITCH VIEW ####
    def switch_view(self, to: VNames) -> None:
        match to:
            case VNames.VIEW_MENU:
                self.show_view(self.vmenu)
            case VNames.VIEW_GAME:
                self.show_view(self.vgame)
            case VNames.VIEW_PAUSE:
                self.show_view(VPause())

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        VData.width = width
        VData.height = height
