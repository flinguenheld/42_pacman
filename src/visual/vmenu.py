from arcade import Vec2
from src.visual.gui.gmenu import GMenu
from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
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
            frame=GFrame(
                atlas=atlas,
                width=800,
                height=800,
                separators=[400],
            ),
        )

        self.menu = GMenu(atlas, ["ONE", "TWO", "THREE"], Vec2(400, 650))

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        super().on_draw()
        with self.camera.activate():
            self.menu.draw()

        # arcade.draw_text("View menu", 100, 100, arcade.color.BLUE, 100)
        # self.manager.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        super().on_update(delta_time)
        self.menu.update(delta_time)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.window.switch_view(VNames.VIEW_GAME)
        # pass
