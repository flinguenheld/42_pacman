import random
import arcade
from arcade import SpriteList, Vec2

from src.visual import VNames, VData
from src.maze.maze_wrapper import Maze
from src.visual.vgamestate import GameState
from src.visual.entities.ventity import VEntity
from src.visual.sprites.vsprite_manager import SpriteManager
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_pacgum import VEntityPacGum


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        arcade.enable_timings()

        self.gamestate = GameState()
        self.sprite_manager = SpriteManager()

        # QUESTION Usefull since it will be replaced in on_resize ??
        self.camera = arcade.Camera2D(self.window.rect)

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Maze --
        self.new_maze(
            random.randint(10, 20),
            random.randint(5, 20),
            random.randint(1, 200),
        )

        # Player --
        self.player_list: SpriteList[VEntity] = arcade.SpriteList()
        self.player: VEntityPlayer = VEntityPlayer(
            self.sprite_manager.atlas,
            "player",
            Vec2(VData.SPRITE_SIZE, VData.SPRITE_SIZE),
            self.sprite_manager.walls,
            self.gamestate,
        )
        self.player_list.append(self.player)

        # Pacgums --
        self.pacgum_list: SpriteList[VEntity] = arcade.SpriteList()
        for floor_sprite in self.sprite_manager.floors.sprites:
            if floor_sprite.position != self.player.position:
                if random.choices([True, False], weights=[70, 30])[0]:
                    position = Vec2(*floor_sprite.position)
                    self.pacgum_list.append(
                        VEntityPacGum(self.sprite_manager.atlas, position)
                    )

    # ########################################################################
    # ########################################################### ON SHOW ####
    def on_show_view(self) -> None:
        arcade.set_background_color(self.sprite_manager.background_color)
        self.reload_current_maze_sprites()

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        self.camera = arcade.Camera2D(self.window.rect)
        self.camera_center()

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, raw_width: int, raw_height: int, seed: int) -> None:
        self.maze_gen = Maze()
        self.maze_gen.generate_new_maze(raw_width, raw_height, seed)
        self.maze_gen.build_walls()
        self.maze_gen.build_floors()
        self.maze_gen.build_background()
        self.reload_current_maze_sprites()

    # ########################################################################
    # #################################################### RELOAD SPRITES ####
    def reload_current_maze_sprites(self) -> None:
        self.sprite_manager.reload(self.maze_gen)
        self.camera_center()

    # ########################################################################
    # ############################################################ CAMERA ####
    def camera_center(self) -> None:
        self.camera.position = self.maze_gen.center_position
        self.camera_adapt_zoom()

    def camera_adapt_zoom(self) -> None:
        margin = VData.CAMERA_MARGIN
        scale_hori = (self.width - margin) / self.maze_gen.width
        scale_vert = (self.height - margin) / self.maze_gen.height

        self.camera.zoom = min(scale_hori, scale_vert)

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()
        self.camera.use()

        self.sprite_manager.draw()

        self.sprite_manager.walls.sprites.draw_hit_boxes(
            color=arcade.color.RED, line_thickness=2
        )

        self.pacgum_list.draw()
        self.pacgum_list.draw_hit_boxes(
            color=arcade.color.WHITE, line_thickness=1
        )

        self.player_list.draw()
        self.player_list.draw_hit_boxes(
            color=arcade.color.RED, line_thickness=1
        )

        # --
        current_fps = arcade.get_fps()
        arcade.draw_text(
            f"FPS: {current_fps:.2f}", 10, 0, arcade.color.WHITE, 22, bold=True
        )

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.player.update(delta_time)
        self.sprite_manager.update(delta_time)

        self.player_list.update_animation(delta_time)
        self.pacgum_list.update_animation(delta_time)

    # ########################################################################
    # #################################################### UP SPRITE SIZE ####
    def up_sprite_size(self, new_size: int) -> None:
        if new_size >= 10:
            VData.SPRITE_SIZE = new_size
            VData.SPRITE_SIZE_BACKGROUND = new_size * 4
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
            self.camera.zoom += 0.1
        elif symbol == arcade.key.MINUS:
            self.camera.zoom -= 0.1
        elif symbol == arcade.key.EQUAL:
            self.camera.zoom = 1.0

        elif symbol == arcade.key.S:
            self.sprite_manager.next_style()
            self.sprite_manager.reload(self.maze_gen, reload_atlas=True)
            arcade.set_background_color(self.sprite_manager.background_color)

        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.player.on_key_release(symbol, modifiers)
