import arcade
import arcade.gui

from src.visual import ViewNames

# GUI tutorial ##
# https://api.arcade.academy/en/latest/tutorials/menu/index.html


class VMenu(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        button_options = arcade.gui.UIFlatButton(text="Options", width=150)
        button_scores = arcade.gui.UIFlatButton(text="Score", width=150)
        button_exit = arcade.gui.UIFlatButton(text="Exit", width=320)

        # Initialise the button with an on_click event.
        @button_options.event("on_click")
        def on_click_options_button(event):
            self.window.switch_view(ViewNames.VIEW_GAME)

        @button_scores.event("on_click")
        def on_click_scores_button(event):
            self.window.switch_view(ViewNames.VIEW_GAME)

        @button_exit.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        grid = arcade.gui.UIGridLayout(
            column_count=2,
            row_count=2,
            horizontal_spacing=20,
            vertical_spacing=20,
        )

        grid.add(button_options, column=0, row=0)
        grid.add(button_scores, column=1, row=0)
        grid.add(button_exit, column=0, row=1, column_span=2)

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=grid,
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.EERIE_BLACK)

        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        # arcade.draw_text("View menu", 100, 100, arcade.color.FRENCH_BLUE, 100)
        self.manager.draw()

    def on_key_press(self, symbol, modifiers):
        self.window.switch_view(ViewNames.VIEW_GAME)
