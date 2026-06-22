from __future__ import annotations
from src.visual.sprites.sforty_two import SFortyTwo

import arcade
from arcade import SpriteList, Vec2

from src.visual.swall import SWall
from src.visual import VNames, VData
from src.maze.maze_wrapper import Maze
from src.visual.sprites.sfloor import SFloor
from src.visual.sprites.sprites import Sprites


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

        # TODO: CREATE A MANAGER #####################
        # TODO: CREATE A MANAGER #####################
        # TODO: CREATE A MANAGER #####################
        self.walls: SWall = SWall()
        self.floors: SFloor = SFloor()
        self.forty_two: SFortyTwo = SFortyTwo()

        self.all_sprites: SpriteList = arcade.SpriteList()

        self.player = arcade.Sprite(VData.SPRITES + "/hen.png", 1)

        self.player.center_y = 150
        self.player.center_x = 150
        # self.player.left = 10
        self.all_sprites.append(self.player)

        self.setup()

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Create a maze
        self.new_maze(42, Vec2(20, 20))

        self.change_style(SWall.Style.Fantasy)
        # self.walls.change_style(WallSprites.Style.Tree)

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, seed: int, size: Vec2) -> None:
        self.maze_gen = Maze(seed, size)
        self.maze_gen.generate_new_maze()
        self.maze_gen.build_walls()
        self.maze_gen.build_path()

    def change_style(self, style: Sprites.Style):
        self.walls.style = style
        self.walls.reload(self.maze_gen.walls)

        # TODO: RENAME MAZE_GEN PATH -> FLOOR ???
        self.floors.style = style
        self.floors.reload(self.maze_gen.paths)

        self.forty_two.style = style
        self.forty_two.reload(self.maze_gen.forty_two)

    # ########################################################################
    # ##################################################### DRAW / UPDATE ####
    def on_draw(self) -> None:
        self.clear()
        self.all_sprites.draw()

        # TODO: add a draw method in SWall ?
        self.walls.sprites.draw()
        self.floors.sprites.draw()
        self.forty_two.sprites.draw()

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

        elif symbol == arcade.key.S:
            match self.walls.current:
                case SWall.Style.Basic:
                    self.walls.change_style(SWall.Style.Tree)
                case SWall.Style.Tree:
                    self.walls.change_style(SWall.Style.PixelWater)
                case SWall.Style.PixelWater:
                    self.walls.change_style(SWall.Style.Basic)

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
