from __future__ import annotations

import arcade
from arcade import SpriteList, Vec2

from src.visual import VNames, VData
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor
from src.visual.sprites.sforty_two import SFortyTwo


# TODO: KEEP ?? - RENAME ?? - MOVE ??
class SpriteManager:
    def __init__(self) -> None:
        self.walls: SWall = SWall()
        self.floors: SFloor = SFloor()
        self.forty_two: SFortyTwo = SFortyTwo()

    def next_style(self) -> None:
        self.walls.next_style()
        self.floors.next_style()
        # self.forty_two.next_style()

    def reload(self, maze: Maze) -> None:
        self.walls.reload(maze.walls.union(maze.forty_two))
        self.floors.reload(maze.floors)
        # self.forty_two.reload(maze.forty_two)

    def draw(self) -> None:
        self.walls.sprites.draw()
        self.floors.sprites.draw()
        # self.forty_two.sprites.draw()


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

        self.sprite_manager = SpriteManager()

        self.sprite_test: SpriteList = arcade.SpriteList()
        self.player = arcade.Sprite(VData.SPRITES + "/hen.png", 1)

        self.player.center_y = 150
        self.player.center_x = 150
        self.sprite_test.append(self.player)

        self.setup()

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Create a maze
        self.new_maze(42, Vec2(15, 15))
        self.sprite_manager.reload(self.maze_gen)

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.WARM_BLACK)

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, seed: int, size: Vec2) -> None:
        self.maze_gen = Maze(seed, size)
        self.maze_gen.generate_new_maze()
        self.maze_gen.build_walls()
        self.maze_gen.build_floors()

    # ########################################################################
    # ##################################################### DRAW / UPDATE ####
    def on_draw(self) -> None:
        self.clear()
        self.sprite_manager.draw()
        self.sprite_test.draw()

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
            self.sprite_manager.next_style()
            self.sprite_manager.reload(self.maze_gen)

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
