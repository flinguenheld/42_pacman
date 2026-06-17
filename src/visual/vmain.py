from __future__ import annotations

import arcade
from src.visual import ViewNames
from src.visual.vgame import VGame
from src.visual.vmenu import VMenu


class VMain(arcade.Window):
    HEIGHT = 800
    WIDTH = 1000

    def __init__(self):
        super().__init__(VMain.WIDTH, self.HEIGHT, "Hello")

        self.vmenu = VMenu()
        self.vgame = VGame()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

        # self.show_view(VMenu())

    def switch_view(self, to: VMain.Views):

        match to:
            case ViewNames.VIEW_MENU:
                self.show_view(self.vmenu)
            case ViewNames.VIEW_GAME:
                self.show_view(self.vgame)
