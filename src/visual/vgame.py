import arcade
from arcade import SpriteList

from src.visual import VNames


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.x = 100
        self.y = 100

        self.vel_x = 0
        self.vel_y = 0

        self.all_sprites: SpriteList = arcade.SpriteList()

        self.player = arcade.Sprite("src/visual/sprites/hen.png", 1)

        self.player.center_y = 150
        self.player.center_x = 150
        # self.player.left = 10
        self.all_sprites.append(self.player)

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    # ########################################################################
    # ##################################################### DRAW / UPDATE ####
    def on_draw(self) -> None:
        self.clear()
        self.all_sprites.draw()

    def on_update(self, delta_time: int | float) -> None:
        speed = 200
        self.player.center_x += self.vel_x * delta_time * speed
        self.player.center_y += self.vel_y * delta_time * speed

        if self.vel_x != 0:
            self.player.angle += 1
        elif self.vel_y != 0:
            self.player.angle -= 1

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:

        if symbol == arcade.key.M:
            self.window.switch_view(VNames.VIEW_MENU)
        elif symbol == arcade.key.P:
            self.window.switch_view(VNames.VIEW_PAUSE)

        elif symbol == arcade.key.LEFT:
            self.vel_x = -1
        elif symbol == arcade.key.RIGHT:
            self.vel_x = 1
        elif symbol == arcade.key.UP:
            self.vel_y = 1
        elif symbol == arcade.key.DOWN:
            self.vel_y = -1

    def on_key_release(self, symbol: int, modifiers: int) -> None:

        self.player.angle += 10

        if symbol == arcade.key.LEFT:
            self.vel_x = 0
        elif symbol == arcade.key.RIGHT:
            self.vel_x = 0
        elif symbol == arcade.key.UP:
            self.vel_y = 0
        elif symbol == arcade.key.DOWN:
            self.vel_y = 0
