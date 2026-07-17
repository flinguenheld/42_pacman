import arcade.gui

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.title.gtitle import GTitle
from src.visual.gui.gbackground import GBackground


class GWindow(arcade.View):
    WIDTH: int = 2000
    HEIGHT: int = 2000

    def __init__(self, atlas: VAtlas, title: GTitle) -> None:
        super().__init__()
        self.atlas = atlas
        self.background = GBackground(atlas)
        self.frame = GFrame(atlas, 0, 0, 1000, 1000)
        arcade.set_background_color(self.atlas.get_color("background"))

        self.title = title

    # ########################################################################
    # ############################################################# Build ####
    # def build(self) -> None:

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()
        self.background.draw()
        self.frame.draw()

        self.title.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.background.update(delta_time)
        self.frame.update(delta_time)
        self.title.update(delta_time)
