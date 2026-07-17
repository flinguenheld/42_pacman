import arcade.gui

from src.visual.vatlas import VAtlas
from src.visual.gui.gbackground import GBackground


class GWindow(arcade.View):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__()
        self.atlas = atlas
        self.background = GBackground(atlas)
        arcade.set_background_color(self.atlas.get_color("background"))

    # ########################################################################
    # ############################################################# Build ####
    # def build(self) -> None:

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()
        self.background.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.background.update(delta_time)
