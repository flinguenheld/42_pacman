from __future__ import annotations
from src.visual.vpause import VPause

import arcade
from src.visual.vgame import VGame
from src.visual.vmenu import VMenu
from src.visual import VNames, VData
from mazegenerator import MazeGenerator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░█▀█░▀█▀░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░░█░░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░░
class VMain(arcade.Window):
    def __init__(self) -> None:
        super().__init__(VData.WIDTH, VData.HEIGHT, "Pac-man")
        self.maze_generator = MazeGenerator()
        self.maze_generator.generate()
        print(self.maze_generator.maze)

        arcade.resources.load_kenney_fonts()

        self.vmenu = VMenu()
        self.vgame = VGame()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""
        pass

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
