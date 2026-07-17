import arcade.gui

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.gbackground import GBackground


class GWindow(arcade.View):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__()
        self.atlas = atlas

        self.background = GBackground(atlas)
        self.frame = GFrame(atlas, 0, 0, 500, 500)

    # ########################################################################
    # ############################################################# Build ####
    def build(self) -> None:
        arcade.set_background_color(self.atlas.get_color("background"))

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()
        self.background.draw()
        self.frame.draw()

    # ########################################################################
    # ############################################################ RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        pass

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.background.update(delta_time)
        self.frame.update(delta_time)
