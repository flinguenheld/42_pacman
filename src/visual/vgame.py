from __future__ import annotations
import time
import random

import arcade
from arcade import SpriteList, Vec2

from src.visual import VNames, VData
from src.visual.vpacgum import PacGum
from src.visual.vplayer import Player
from src.maze.maze_wrapper import Maze
from src.visual.sprites.vsprite_manager import SpriteManager
from src.utils.maze_grid_to_world_coords import maze_grid_to_world_coords


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.sprite_manager = SpriteManager()
        self.camera = arcade.Camera2D(
            viewport=arcade.types.Viewport(
                left=0,
                bottom=0,
                width=VData.WIDTH,
                height=VData.HEIGHT,
            )
        )
        self.player: Player | None = None
        self.player_sprite_list: SpriteList[Player] | None = None

        self.pacgum_list: SpriteList[PacGum] | None = None
        self.setup()
        # self.camera.use()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Create a maze
        self.new_maze(
            random.randint(10, 30),
            random.randint(5, 30),
            random.randint(1, 200),
        )
        self.sprite_manager.reload(self.maze_gen)
        self.player = Player(
            Maze.to_world_coords(Vec2(2, 2), scale=2.0),
            self.sprite_manager.walls,
        )

        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player)

        self.pacgum_list = arcade.SpriteList()
        # for floor in self.maze_gen.floors:
        #     if floor == self.maze_gen.entry or floor == self.maze_gen.exit:
        #         continue
        #     self.pacgum_list.append(
        #         PacGum(floor * VData.SPRITE_SIZE + VData.SPRITE_SHIFT)
        #     )

    # ########################################################################
    # ########################################################### ON SHOW ####
    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.WARM_BLACK)

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, width: int, height: int, seed: int) -> None:
        self.maze_gen = Maze()
        self.maze_gen.generate_new_maze(width, height, seed)
        self.maze_gen.build_walls()
        self.maze_gen.build_floors()
        self.maze_gen.build_background()

    # ########################################################################
    # ################################################ REBUILD BACKGROUND ####
    def rebuild_background(self):
        self.maze_gen.build_background()
        self.sprite_manager.reload(self.maze_gen)

    # ########################################################################
    # ##################################################### DRAW / UPDATE ####
    def on_draw(self) -> None:
        assert self.player_sprite_list is not None, (
            "Player sprite list is not initialized"
        )
        assert self.pacgum_list is not None, (
            "PacGum sprite list is not initialized"
        )
        self.clear()

        # Activate our camera before drawing
        # self.camera.use()

        self.sprite_manager.draw()
        self.player_sprite_list.draw()
        self.player_sprite_list.draw_hit_boxes(
            color=arcade.color.RED, line_thickness=2
        )
        # self.pacgum_list.draw()
        # self.pacgum_list.draw_hit_boxes(
        #     color=arcade.color.GREEN, line_thickness=2
        # )

    def on_update(self, delta_time: int | float) -> None:
        assert self.player is not None, "Player is not initialized"
        self.player.update(delta_time)

        # self.camera.position = Maze.center_point()

        # TEST #############################################
        # TEST #############################################
        # TEST #############################################
        self.sprite_manager.update(delta_time)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:

        if symbol == arcade.key.M:
            self.window.switch_view(VNames.VIEW_MENU)
        elif symbol == arcade.key.P:
            self.window.switch_view(VNames.VIEW_PAUSE)

        elif symbol == arcade.key.N:
            self.setup()

        elif symbol == arcade.key.S:
            self.sprite_manager.next_style()
            self.sprite_manager.reload(self.maze_gen)

        assert self.player is not None, "Player is not initialized"
        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        assert self.player is not None, "Player is not initialized"
        self.player.on_key_release(symbol, modifiers)
