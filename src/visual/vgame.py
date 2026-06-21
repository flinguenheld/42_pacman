import arcade
from arcade import SpriteList, Vec2

from src.visual import VNames, VData
from src.maze.maze_wrapper import Maze


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

        self.walls: SpriteList = arcade.SpriteList()
        self.all_sprites: SpriteList = arcade.SpriteList()

        self.player = arcade.Sprite(VData.SPRITES + "hen.png", 1)

        self.player.center_y = 150
        self.player.center_x = 150
        # self.player.left = 10
        self.all_sprites.append(self.player)

        self.setup()

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        self.maze_gen = Maze(42, Vec2(15, 15))
        self.maze_gen.generate_new_maze()
        self.maze_gen.build_maze()

        for point, value in self.maze_gen.maze.items():
            self.walls.append(
                arcade.Sprite(
                    path_or_texture=f"{VData.SPRITES}wall_{value}.png",
                    center_x=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.x,
                    center_y=VData.SPRITE_SHIFT + VData.SPRITE_SIZE * point.y,
                )
            )

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    # ########################################################################
    # ##################################################### DRAW / UPDATE ####
    def on_draw(self) -> None:
        self.clear()
        self.all_sprites.draw()
        self.walls.draw()

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
