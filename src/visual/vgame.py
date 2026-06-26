from __future__ import annotations
from src.visual.vatlas import VAtlas

import arcade
from arcade import SpriteList, Vec2

from src.visual import VNames, VData
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor
from src.visual.vplayer import Player


# TODO: KEEP ?? - RENAME ?? - MOVE ??
class SpriteManager:
    def __init__(self) -> None:
        self.atlas = VAtlas()
        self.walls: SWall = SWall(self.atlas)
        # self.floors: SFloor = SFloor()

    def next_style(self) -> None:
        # self.walls.next_style()
        # self.floors.next_style()
        self.atlas.next_style()

    def reload(self, maze: Maze) -> None:

        self.atlas.load_info()
        self.atlas.load_textures()
        self.walls.reload(maze.walls.union(maze.forty_two), maze.floors)
        # self.floors.reload(maze.floors)

        # def draw(self) -> None:

        # scale = 3
        # y = 100
        # self.sprite_list = SpriteList()
        # for entry, textures in self.atlas.textures.items():
        #     y += 16 * scale
        #     x = 100
        #     print(f"nb textures: {len(textures)}   new line -> {entry}")

        #     # REGULAR -----------------------------------
        #     for tex in textures:
        #         # print("add one")

        #         if isinstance(tex, arcade.TextureAnimation):
        #             sprite = arcade.TextureAnimationSprite(
        #                 animation=tex,
        #                 scale=scale,
        #                 center_x=x,
        #                 center_y=y,
        #             )
        #         else:
        #             sprite = arcade.Sprite(
        #                 path_or_texture=tex,
        #                 scale=scale,
        #                 center_x=x,
        #                 center_y=y,
        #             )

        #         self.sprite_list.append(sprite)
        #         x += 16 * scale

    def update(self, delta_time):
        # self.sprite_list.update_animation(delta_time)
        self.walls.update_animation(delta_time)

    def draw(self) -> None:
        # self.sprite_list.draw()
        # print("blah")

        # pass
        self.walls.sprites.draw()
        # self.floors.sprites.draw()


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

        self.setup()
        self.camera.use()

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Create a maze
        self.new_maze(42, Vec2(15, 15))
        self.sprite_manager.reload(self.maze_gen)
        self.player = Player(self.maze_gen.entry, self.sprite_manager.walls)

        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player)

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
        assert self.player_sprite_list is not None, (
            "Player sprite list is not initialized"
        )
        self.clear()
        self.sprite_manager.draw()
        self.player_sprite_list.draw()
        self.player_sprite_list.draw_hit_boxes(
            color=arcade.color.RED, line_thickness=2
        )

    def on_update(self, delta_time: int | float) -> None:
        assert self.player is not None, "Player is not initialized"
        self.player.update(delta_time)

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

        elif symbol == arcade.key.S:
            self.sprite_manager.next_style()
            self.sprite_manager.reload(self.maze_gen)

        assert self.player is not None, "Player is not initialized"
        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        assert self.player is not None, "Player is not initialized"
        self.player.on_key_release(symbol, modifiers)
