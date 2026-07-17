from arcade import Vec2
from src.visual.gui.gframe import GFrame
import arcade.gui

from src.visual.vatlas import VAtlas
from src.visual.gui.gbackground import GBackground


class TestTitle:
    def __init__(self):

        self.walls: set[Vec2] = set()
        self.floors: set[Vec2] = set()

        title = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        for y, row in enumerate(reversed(title)):
            for x, value in enumerate(row):
                if value == 0:
                    self.walls.add(Vec2(x, y))
                else:
                    self.floors.add(Vec2(x, y))


class GWindow(arcade.View):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__()
        self.atlas = atlas
        self.background = GBackground(atlas)
        self.frame = GFrame(atlas, 0, 0, 500, 500)
        arcade.set_background_color(self.atlas.get_color("background"))

    # ########################################################################
    # ############################################################# Build ####
    # def build(self) -> None:

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()
        self.background.draw()
        self.frame.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.background.update(delta_time)
        self.frame.update(delta_time)
