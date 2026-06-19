import arcade
import arcade.key
from src.visual import VData, VNames


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀█░█░█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█▀█░█░█░▀▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░
class VPause(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.text = "PAUSE"
        self.letters = []
        self.current_index: int = -1
        self.time_elapsed: float = 0.0

        pos = VData.CENTER_X - (len(self.text) * VData.FONT_SIZE_TITLE) // 2
        for letter in self.text:
            self.letters.append(
                arcade.Text(
                    letter,
                    x=pos,
                    y=VData.CENTER_Y,
                    color=arcade.color.BLACK,
                    font_size=VData.FONT_SIZE_TITLE,
                    anchor_x="center",
                    anchor_y="center",
                    font_name="Kenney Blocks",
                )
            )
            pos += VData.FONT_SIZE_TITLE

    # ########################################################################
    # ###################################################### ON SHOW VIEW ####
    # TODO: useless ? put that in init or not ?
    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.ANTIQUE_WHITE)

    # ########################################################################
    # ######################################################### ON UPDATE ####
    def on_update(self, delta_time: float) -> None:
        self.time_elapsed += delta_time

        if self.time_elapsed > 0.25 or self.current_index == -1:
            self.time_elapsed = 0.0

            self.current_index = (self.current_index + 1) % len(self.text)

            for i, letter in enumerate(self.letters):
                if i == self.current_index:
                    letter.color = arcade.color.CYBER_YELLOW
                else:
                    letter.color = arcade.color.BLACK

    # ########################################################################
    # ########################################################### ON DRAW ####
    def on_draw(self) -> None:
        self.clear()
        for letter in self.letters:
            letter.draw()

    # ########################################################################
    # #################################################### ON MOUSE / KEY ####
    def on_mouse_press(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int,
    ) -> None:
        self.window.switch_view(VNames.VIEW_GAME)

    def on_key_press(self, symbol: int, modifiers: int) -> None:

        if symbol in [arcade.key.SPACE, arcade.key.ENTER]:
            self.window.switch_view(VNames.VIEW_GAME)

        elif symbol in [arcade.key.Q, arcade.key.M]:
            self.window.switch_view(VNames.VIEW_MENU)
