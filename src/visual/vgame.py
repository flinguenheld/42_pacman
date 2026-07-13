import random
import arcade
from arcade import SpriteList, Vec2

from src.visual.vhud import VHud
from src.maze.maze_wrapper import Maze
from src.visual.vdata import VNames, VData
from src.visual.vgamestate import VGameState
from src.visual.entities.ventity_enemy import VEntityEnemy
from src.visual.sprites.vsprite_manager import SpriteManager
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_pacgum import VEntityPacGum
from src.visual.entities.ventity_super_pacgum import VEntitySuperPacGum


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        arcade.enable_timings()

        self.display_hitboxes = False
        self.sprite_manager = SpriteManager()

        # QUESTION Usefull since it will be replaced in on_resize ??
        self.camera = arcade.Camera2D(self.window.rect)

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Game state --
        self.gamestate = VGameState()

        # HUD --
        self.hud = VHud(self.gamestate)

        # Maze --
        self.new_maze(
            random.randint(10, 20),
            random.randint(5, 20),
            random.randint(1, 200),
        )

        # Init sprite lists first --
        self.enemy_list: SpriteList[VEntityEnemy] = arcade.SpriteList()
        self.player_list: SpriteList[VEntityPlayer] = arcade.SpriteList()
        self.pacgum_list: SpriteList[VEntityPacGum | VEntitySuperPacGum] = (
            arcade.SpriteList()
        )

        # Player --
        self.player: VEntityPlayer = VEntityPlayer(
            self.sprite_manager.atlas,
            self.maze_gen.floor_center,
            self.sprite_manager.walls,
            self.gamestate,
        )
        self.player_list.append(self.player)

        # Enemies --
        for id, floor_corner in enumerate(self.maze_gen.floor_corners):
            self.enemy_list.append(
                VEntityEnemy(
                    id,
                    self.sprite_manager.atlas,
                    floor_corner,
                    self.sprite_manager.floors,
                    self.sprite_manager.walls,
                    self.player,
                )
            )

        # Super pacgums --
        for floor_corner in self.maze_gen.floor_corners:
            self.pacgum_list.append(
                VEntitySuperPacGum(self.sprite_manager.atlas, floor_corner)
            )

        # Pacgums --
        forbbiden = set(self.maze_gen.floor_corners)
        forbbiden.add(Vec2(*self.player.position))

        for floor_sprite in self.sprite_manager.floors.sprites:
            if floor_sprite.position not in forbbiden:
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
        self.hud.on_resize(width, height)

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
        # TODO: Investigate issue with camera centering on smaller maze sizes
        # and bigger sized windows.
        hud_bg_height = self.hud.hud_bg_sprite.height

        self.camera.position = self.maze_gen.center_position
        self.camera.position += Vec2(0, hud_bg_height / 2)
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

        # Separate what is drawn in the camera and
        # what is drawn on the screen itself (HUD, debug info, etc.)

        # Activate the camera, but only inside this 'with' statement.
        with self.camera.activate():
            self.sprite_manager.draw()
            self.pacgum_list.draw(pixelated=True)
            self.player_list.draw(pixelated=True)
            self.enemy_list.draw(pixelated=True)
            self._draw_hitboxes()

        # Camera stops being active
        # We can now draw things like the HUD, etc...
        self.hud.draw()

    # ########################################################################
    # ##################################################### DRAW HITBOXES ####
    def _draw_hitboxes(self) -> None:
        if self.display_hitboxes:
            self.sprite_manager.walls.sprites.draw_hit_boxes(
                color=arcade.color.RED, line_thickness=2
            )
            self.pacgum_list.draw_hit_boxes(
                color=arcade.color.WHITE, line_thickness=1
            )
            self.player_list.draw_hit_boxes(
                color=arcade.color.GRANNY_SMITH_APPLE, line_thickness=2
            )
            self.enemy_list.draw_hit_boxes(
                color=arcade.color.AFRICAN_VIOLET, line_thickness=2
            )

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.enemy_list.update(delta_time)
        self.player_list.update(delta_time)
        self.sprite_manager.update(delta_time)
        self.resolve_player_pacgum_collisions()

        self.enemy_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)
        self.pacgum_list.update_animation(delta_time)

    # ########################################################################
    # ########################################## PLAYER PACGUM COLLISIONS ####
    def resolve_player_pacgum_collisions(self) -> None:
        collided: list[VEntityPacGum | VEntitySuperPacGum] = (
            arcade.check_for_collision_with_list(self.player, self.pacgum_list)
        )
        for pacgum in collided:
            self.gamestate.increment_score(pacgum.get_points())
            pacgum.kill()

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Player movement is handled in the player class.
        # The WASD, ZQSD and arrow keys are reserved for player movement.

        match symbol:
            case arcade.key.M:
                self.window.switch_view(VNames.VIEW_MENU)
            case arcade.key.P:
                self.window.switch_view(VNames.VIEW_PAUSE)

            case arcade.key.N:
                self.setup()

            case arcade.key.H:
                self.display_hitboxes = not self.display_hitboxes

            case arcade.key.PLUS:
                self.camera.zoom += 0.1
            case arcade.key.MINUS:
                self.camera.zoom -= 0.1
            case arcade.key.EQUAL:
                self.camera.zoom = 1.0

        # TODO: reimplement style switching feature and change key
        # elif symbol == arcade.key.S:
        #     self.sprite_manager.next_style()
        #     self.sprite_manager.reload(self.maze_gen, reload_atlas=True)
        #     arcade.set_background_color(self.sprite_manager.background_color)

        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.player.on_key_release(symbol, modifiers)
