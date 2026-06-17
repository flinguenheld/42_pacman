import arcade

from src.visual import ViewNames


class VGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.x = 100
        self.y = 100

        self.vel_x = 0
        self.vel_y = 0

        self.all_sprites = arcade.SpriteList()

        # def setup(self):
        # def on_show_view(self):
        """Set up the game here. Call this function to restart the game."""

        self.player = arcade.Sprite("src/visual/sprites/hen.png", 1)

        self.player.center_y = 150
        self.player.center_x = 150
        # self.player.left = 10
        self.all_sprites.append(self.player)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def on_draw(self):
        """Draw everything"""
        self.clear()

        self.all_sprites.draw()

        # arcade.finish_render()

    def on_update(self, delta_time):
        speed = 200
        self.player.center_x += self.vel_x * delta_time * speed
        self.player.center_y += self.vel_y * delta_time * speed

        if self.vel_x != 0:
            self.player.angle += 1
        elif self.vel_y != 0:
            self.player.angle -= 1

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.vel_x = -1
        if symbol == arcade.key.RIGHT:
            self.vel_x = 1
        if symbol == arcade.key.UP:
            self.vel_y = 1
        if symbol == arcade.key.DOWN:
            self.vel_y = -1

        if symbol == arcade.key.M:
            self.window.switch_view(ViewNames.VIEW_MENU)

    def on_key_release(self, symbol, modifiers):

        self.player.angle += 10

        if symbol == arcade.key.LEFT:
            self.vel_x = 0
        if symbol == arcade.key.RIGHT:
            self.vel_x = 0
        if symbol == arcade.key.UP:
            self.vel_y = 0
        if symbol == arcade.key.DOWN:
            self.vel_y = 0
