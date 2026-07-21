import random
import arcade
from arcade.types import Color
from arcade import SpriteList, Vec2, LBWH

from src.visual.vhud import VHud
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.vdata import VNames, VData
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor
from src.visual.vgamestate import VGameState
from src.visual.entities.ventity_enemy import (
    Charlie,
    EnemyVariant,
    Johnny,
    Michael,
    ReverseMichael,
    VEntityEnemyCommon,
)
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_pacgum import VEntityPacGum
from src.visual.entities.ventity_super_pacgum import VEntitySuperPacGum


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__()
        arcade.enable_timings()

        self.atlas = atlas
        self.setup_done = False
        arcade.set_background_color(self.atlas.get_color("background"))

        self.process_updates = True
        self.display_hitboxes = False
        self.display_enemy_paths = False

        self.camera = arcade.Camera2D()
        self.camera_hud = arcade.Camera2D()

        from src.visual.vmain import VMain

        self.window: VMain = self.window  # type: ignore

        # Game state --
        # Needs to be initialized here as it is reused for every game
        # and should not be reset every time setup() is called.
        self.gamestate = VGameState()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Restart the game."""

        self.setup_done = False

        # Maze spritelists --
        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas)

        # Maze --
        self.new_maze(
            random.randint(10, 20),
            random.randint(5, 20),
            random.randint(1, 200),
        )

        # HUD --
        self.hud = VHud(
            self.maze_gen,
            self.atlas,
            self.gamestate,
        )

        # Init sprite lists first --
        self.enemy_list: SpriteList[VEntityEnemyCommon] = arcade.SpriteList()
        self.player_list: SpriteList[VEntityPlayer] = arcade.SpriteList()
        self.pacgum_list: SpriteList[VEntityPacGum | VEntitySuperPacGum] = (
            arcade.SpriteList()
        )

        # Player --
        self.player: VEntityPlayer = VEntityPlayer(
            self.atlas,
            self.maze_gen.floor_center,
            self.walls,
            self.gamestate,
        )
        self.player_list.append(self.player)

        ennemies: tuple[
            EnemyVariant,
            EnemyVariant,
            EnemyVariant,
            EnemyVariant,
        ] = (
            Michael,
            Johnny,
            Charlie,
            ReverseMichael,
        )
        # Enemies --
        for ennemy, floor_corner in zip(ennemies, self.maze_gen.floor_corners):
            self.enemy_list.append(
                ennemy(
                    self.atlas,
                    floor_corner,
                    self.floors,
                    self.walls,
                    self.player,
                    self.gamestate,
                    self.maze_gen,
                ),
            )

        # Super pacgums --
        for floor_corner in self.maze_gen.floor_corners:
            self.pacgum_list.append(
                VEntitySuperPacGum(self.atlas, floor_corner)
            )

        # Pacgums --
        forbbiden = set(self.maze_gen.floor_corners)
        forbbiden.add(Vec2(*self.player.position))

        for floor_sprite in self.floors.sprites:
            if floor_sprite.position not in forbbiden:
                if random.choices([True, False], weights=[70, 30])[0]:
                    position = Vec2(*floor_sprite.position)
                    self.pacgum_list.append(
                        VEntityPacGum(self.atlas, position)
                    )

        self.setup_done = True

    # ########################################################################
    # ########################################################### ON SHOW ####
    def on_show_view(self) -> None:
        self.setup()
        self.cameras_update()

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        if self.setup_done:
            self.cameras_update()

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, raw_width: int, raw_height: int, seed: int) -> None:
        self.maze_gen = Maze()
        self.maze_gen.generate_new_maze(raw_width, raw_height, seed)
        self.maze_gen.build_walls()
        self.maze_gen.build_floors()
        self.reload_maze_sprites()

    # ########################################################################
    # #################################################### RELOAD SPRITES ####
    def reload_maze_sprites(self) -> None:
        self.walls.reload(
            self.maze_gen.walls.union(self.maze_gen.forty_two),
            self.maze_gen.floors,
        )
        self.floors.reload(self.maze_gen.floors)
        self.cameras_update()

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        if self.setup_done:
            self.clear()
            with self.camera.activate():
                self.walls.draw()
                self.floors.draw()
                self.pacgum_list.draw(pixelated=True)
                self.player_list.draw(pixelated=True)
                self.enemy_list.draw(pixelated=True)
                self._draw_hitboxes()
                self._draw_enemy_paths()

            with self.camera_hud.activate():
                self.hud.draw()

    # ########################################################################
    # ##################################################### DRAW HITBOXES ####
    def _draw_hitboxes(self) -> None:
        if self.display_hitboxes:
            self.walls.sprites.draw_hit_boxes(
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

    def _draw_enemy_paths(self) -> None:
        colors: tuple[Color, Color, Color, Color] = (
            arcade.color.RED,
            arcade.color.GREEN,
            arcade.color.BLUE,
            arcade.color.YELLOW,
        )
        line_width = 20
        if self.display_enemy_paths:
            for color, enemy in zip(colors, self.enemy_list):
                if not enemy.path:
                    continue
                arcade.draw_line_strip(
                    [Vec2(*enemy.position)] + enemy.path,
                    color,
                    line_width,
                )
                line_width -= 5

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        if self.setup_done and self.process_updates:
            self.handle_player_death()

            self.walls.update(delta_time)
            self.floors.update(delta_time)
            self.enemy_list.update(delta_time)
            self.player_list.update(delta_time)
            self.resolve_player_pacgum_collisions()
            self.resolve_player_enemy_collisions()

            self.enemy_list.update_animation(delta_time)
            self.player_list.update_animation(delta_time)
            self.pacgum_list.update_animation(delta_time)

            self.hud.update(delta_time)

    def is_player_dead(self) -> bool:
        return self.player not in self.player_list

    def handle_player_death(self) -> None:
        if self.is_player_dead():
            self.gamestate.decrement_lives()
            if self.gamestate.is_game_over():
                self.window.switch_view(VNames.VIEW_WELCOME)
            else:
                self.setup()
                self.cameras_update()

    # ########################################################################
    # ########################################## PLAYER PACGUM COLLISIONS ####
    def resolve_player_pacgum_collisions(self) -> None:
        collided: list[VEntityPacGum | VEntitySuperPacGum] = (
            arcade.check_for_collision_with_list(self.player, self.pacgum_list)
        )
        for pacgum in collided:
            self.gamestate.increment_score(pacgum.get_points())
            pacgum.kill()

    def resolve_player_enemy_collisions(self) -> None:
        collided: list[VEntityEnemyCommon] = (
            arcade.check_for_collision_with_list(self.player, self.enemy_list)
        )
        for _enemy in collided:
            self.player.kill()

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Player movement is handled in the player class.
        # The WASD, ZQSD and arrow keys are reserved for player movement.

        if self.setup_done:
            match symbol:
                case arcade.key.ESCAPE:
                    arcade.exit()

                case arcade.key.M:
                    self.window.switch_view(VNames.VIEW_WELCOME)
                case arcade.key.P:
                    self.window.switch_view(VNames.VIEW_PAUSE)

                case arcade.key.N:
                    self.setup()
                    self.cameras_update()

                # TODO: Potentially replace the current pause view with this
                # for pausing the game?
                case arcade.key.SPACE:
                    self.process_updates = not self.process_updates

                case arcade.key.H:
                    self.display_hitboxes = not self.display_hitboxes
                    self.display_enemy_paths = not self.display_enemy_paths
                    VData.debug_on = not VData.debug_on
                case arcade.key.H:
                    self.display_hitboxes = not self.display_hitboxes
                    VData.debug_on = not VData.debug_on
                case _:
                    pass

            # TODO: reimplement style switching feature and change key
            # elif symbol == arcade.key.S:
            #     self.sprite_manager.next_style()
            #     self.sprite_manager.reload(self.maze_gen, reload_atlas=True)
            #     arcade.set_background_color(self.sprite_manager.background_color)

            self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if self.setup_done:
            self.player.on_key_release(symbol, modifiers)

    # ########################################################################
    # ########################################################### CAMERAS ####
    def cameras_update(self) -> None:
        def cameras_setup() -> None:
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

        def cameras_zoom() -> None:
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

        # --
        cameras_setup()
        cameras_zoom()
