from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.gui.gwindow import GWindow
from src.visual.gui.title.gtitle_pacman import GTitlePacman


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░█▀▀░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀▀░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class VMenu(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitlePacman(atlas),
            frame_size=Vec2(800, 600),
        )
        pass

        # From bottom to top --
        # self.widgets["frame_scores"] = GFrame(
        #     atlas, x=0, y=0, width=900, height=600
        # )
        # self.widgets["frame_menu"] = GFrame(
        #     atlas, x=0, y=700, width=900, height=500
        # )
        # self.widgets["title"].set_postion(center_x=500, center_y=1400)

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        super().on_draw()

        # arcade.draw_text("View menu", 100, 100, arcade.color.BLUE, 100)
        # self.manager.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        pass
        # super().update(delta_time)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # self.window.switch_view(VNames.VIEW_GAME)
        pass
