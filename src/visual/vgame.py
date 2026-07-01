import random
import arcade
from arcade import SpriteList, Vec2

from src.visual import VNames, VData
from src.visual.vpacgum import PacGum
from src.visual.vplayer import Player
from src.maze.maze_wrapper import Maze
from src.visual.sprites.vsprite_manager import SpriteManager


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

        self.player = Player(
            Maze.to_world_coords(Vec2(2, 2)),
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
        self.reload_current_maze_sprites()

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, width: int, height: int, seed: int) -> None:
        self.maze_gen = Maze()
        self.maze_gen.generate_new_maze(width, height, seed)
        self.maze_gen.build_walls()
        self.maze_gen.build_floors()
        self.reload_current_maze_sprites()

    # ########################################################################
    # #################################################### RELOAD SPRITES ####
    def reload_current_maze_sprites(self) -> None:
        self.maze_gen.build_background()
        self.sprite_manager.reload(self.maze_gen)
        self.sprite_manager.reload_background(self.maze_gen)

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()

        assert self.player_sprite_list is not None, (
            "Player sprite list is not initialized"
        )
        assert self.pacgum_list is not None, (
            "PacGum sprite list is not initialized"
        )

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

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        assert self.player is not None, "Player is not initialized"
        self.player.update(delta_time)

        # self.camera.position = Maze.center_point()

        self.sprite_manager.update(delta_time)

    # ########################################################################
    # #################################################### UP SPRITE SIZE ####
    def up_sprite_size(self, new_size: int) -> None:
        if new_size >= 10:
            VData.SPRITE_SIZE = new_size
            self.reload_current_maze_sprites()

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:

        if symbol == arcade.key.M:
            self.window.switch_view(VNames.VIEW_MENU)
        elif symbol == arcade.key.P:
            self.window.switch_view(VNames.VIEW_PAUSE)

        elif symbol == arcade.key.N:
            self.setup()

        elif symbol == arcade.key.PLUS:
            self.up_sprite_size(VData.SPRITE_SIZE + 2)
        elif symbol == arcade.key.MINUS:
            self.up_sprite_size(VData.SPRITE_SIZE - 2)
        elif symbol == arcade.key.EQUAL:
            self.up_sprite_size(32)

        elif symbol == arcade.key.S:
            self.sprite_manager.next_style()
            self.sprite_manager.reload(self.maze_gen, reload_atlas=True)
            self.sprite_manager.reload_background(self.maze_gen)

        assert self.player is not None, "Player is not initialized"
        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        assert self.player is not None, "Player is not initialized"
        self.player.on_key_release(symbol, modifiers)
