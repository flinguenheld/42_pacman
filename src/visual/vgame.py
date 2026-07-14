import random
import arcade
from arcade import SpriteList, Vec2, LBWH

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

        self.setup_done = False
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""

        # Game state --
        self.gamestate = VGameState()

        # Maze --
        self.new_maze(
            random.randint(10, 20),
            random.randint(5, 20),
            random.randint(1, 200),
        )

        # HUD --
        self.hud = VHud(
            self.maze_gen,
            self.sprite_manager.atlas,
            self.gamestate,
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
                    self.gamestate,
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

        self.setup_done = True

    # ########################################################################
    # ########################################################### ON SHOW ####
    def on_show_view(self) -> None:
        arcade.set_background_color(self.sprite_manager.background_color)
        self.reload_current_maze_sprites()

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        if self.setup_done:
            self.camera_init()
            self.camera_zoom()

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
        self.camera_init()
        self.camera_zoom()

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()

        if self.setup_done:
            with self.camera.activate():
                self.sprite_manager.draw()
                self.pacgum_list.draw(pixelated=True)
                self.player_list.draw(pixelated=True)
                self.enemy_list.draw(pixelated=True)
                self._draw_hitboxes()

            with self.camera_hud.activate():
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

        self.hud.update(delta_time)

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
            case arcade.key.ESCAPE:
                arcade.exit()

            case arcade.key.M:
                self.window.switch_view(VNames.VIEW_MENU)
            case arcade.key.P:
                self.window.switch_view(VNames.VIEW_PAUSE)

            case arcade.key.N:
                self.setup()
                self.camera_init()
                self.camera_zoom()

            case arcade.key.H:
                self.display_hitboxes = not self.display_hitboxes
                VData.debug_on = not VData.debug_on

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

    # ########################################################################
    # ########################################################### CAMERAS ####
    def camera_init(self) -> None:
        if self.setup_done:
            hud_height = self.height / 8

            main_rect = LBWH(
                left=0,
                bottom=0,
                width=self.width,
                height=self.height - hud_height,
            )
            hud_rect = LBWH(
                left=0,
                bottom=self.height - hud_height,
                width=self.width,
                height=hud_height,
            )

            self.camera = arcade.Camera2D(main_rect)
            self.camera.position = self.maze_gen.center_position

            self.camera_hud = arcade.Camera2D(hud_rect)
            self.camera_hud.position = self.hud.center_position

    def camera_zoom(self) -> None:
        if self.setup_done:
            scale_hori = (
                self.camera.viewport.width - VData.CAMERA_MARGIN
            ) / self.maze_gen.width
            scale_vert = (
                self.camera.viewport.height - VData.CAMERA_MARGIN
            ) / self.maze_gen.height

            zoom = min(scale_hori, scale_vert)
            if zoom > VData.CAMERA_MAX_ZOOM:
                zoom = VData.CAMERA_MAX_ZOOM

            self.camera.zoom = zoom
            self.camera_hud.zoom = zoom
