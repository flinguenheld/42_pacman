from src.visual.gui.title.gtitle_pacman import GTitlePacman
from src.visual.vatlas import VAtlas
from src.visual.gui.gwindow import GWindow
import arcade
import arcade.gui
from arcade.gui import UIEvent

from src.visual.vdata import VNames

# GUI tutorial ##
# https://api.arcade.academy/en/latest/tutorials/menu/index.html


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░█▀▀░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀▀░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class VMenu(GWindow):
    BT_WIDTH = 200
    BT_HEIGHT = BT_WIDTH // 3
    BT_MARGIN = 20
    BT_DOUBLE = BT_WIDTH * 2 + BT_MARGIN

    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(atlas, GTitlePacman(atlas))

        bt_play = arcade.gui.UIFlatButton(
            text="Play",
            width=VMenu.BT_DOUBLE,
            height=VMenu.BT_HEIGHT,
        )
        bt_options = arcade.gui.UIFlatButton(
            text="Options",
            width=VMenu.BT_WIDTH,
            height=VMenu.BT_HEIGHT,
        )
        bt_scores = arcade.gui.UIFlatButton(
            text="Score",
            width=VMenu.BT_WIDTH,
            height=VMenu.BT_HEIGHT,
        )
        bt_exit = arcade.gui.UIFlatButton(
            text="Exit",
            width=VMenu.BT_DOUBLE,
            height=VMenu.BT_HEIGHT,
        )

        # button events --
        @bt_play.event("on_click")
        def on_click_play_button(event: UIEvent) -> None:
            self.window.switch_view(VNames.VIEW_GAME)

        @bt_options.event("on_click")
        def on_click_options_button(event: UIEvent) -> None:
            self.window.switch_view(VNames.VIEW_GAME)

        @bt_scores.event("on_click")
        def on_click_scores_button(event: UIEvent) -> None:
            self.window.switch_view(VNames.VIEW_GAME)

        @bt_exit.event("on_click")
        def on_click_exit_button(event: UIEvent) -> None:
            arcade.exit()

        # Layout --
        grid = arcade.gui.UIGridLayout(
            column_count=2,
            row_count=3,
            horizontal_spacing=VMenu.BT_MARGIN,
            vertical_spacing=VMenu.BT_MARGIN,
        )

        grid.add(bt_play, column=0, row=0, column_span=2)
        grid.add(bt_options, column=0, row=1)
        grid.add(bt_scores, column=1, row=1)
        grid.add(bt_exit, column=0, row=2, column_span=2)

        self.manager = arcade.gui.UIManager()
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=grid,
        )

    # ########################################################################
    # ####################################################### SHOW / HIDE ####
    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.manager.disable()

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        super().on_draw()

        # arcade.draw_text("View menu", 100, 100, arcade.color.BLUE, 100)
        self.manager.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        pass
        # super().update(delta_time)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.window.switch_view(VNames.VIEW_GAME)
