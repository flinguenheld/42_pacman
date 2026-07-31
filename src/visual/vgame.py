import time
import random
import arcade
from arcade.types import Color
from arcade import SpriteList, Vec2, LBWH

from src.maze.maze import Maze
from src.visual.vatlas import VAtlas
from src.visual.gui.ghud import GHud
from src.visual.gamestate import GameState
from src.visual.vdata import VNames, VData
from src.visual.pathfinding.bfs import BFS
from src.visual.gui.gbackground import GBackground
from src.visual.entities.venemy_variants import (
    Charlie,
    EnemyVariant,
    EnemyVariantClass,
    Johnny,
    Michael,
    ReverseMichael,
)
from src.maze.maze_wrapper import MazeGeneratorWrapper
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_pacgum import VEntityPacGum
from src.visual.entities.ventity_enemy import VEntityEnemyCommon
from src.visual.entities.ventity_super_pacgum import VEntitySuperPacGum


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    ENEMY_ORDER: tuple[EnemyVariantClass, ...] = (
        Johnny,
        Michael,
        Charlie,
        ReverseMichael,
    )

    def __init__(self, atlas: VAtlas, gamestate: GameState) -> None:
        super().__init__()

        self.atlas = atlas
        self.setup_done = False

        self.process_updates = True
        self.display_hitboxes = False
        self.display_enemy_paths = False

        self.camera = arcade.Camera2D()
        self.camera_hud = arcade.Camera2D()

        self.gamestate = gamestate

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Restart the game."""

        # TODO: Implement the logic when the level is done
        # TODO:   -> Call setup and level - 1

        self.setup_done = False

        # Maze --
        self.new_maze(
            random.randint(10, 20),
            random.randint(5, 20),
            random.randint(1, 200),
        )

        # Background --
        self.background = GBackground(self.atlas)
        self.background.build(self.maze.center_position, self.maze.rect)
        arcade.set_background_color(self.atlas.get_color("background"))

        # HUD --
        self.hud = GHud(
            self.maze,
            self.atlas,
            self.gamestate,
        )

        # Init sprite lists first --
        self.enemy_list: SpriteList[EnemyVariant] = arcade.SpriteList()
        self.player_list: SpriteList[VEntityPlayer] = arcade.SpriteList()
        self.pacgum_list: SpriteList[VEntityPacGum | VEntitySuperPacGum] = (
            arcade.SpriteList()
        )

        # Player --
        self.player: VEntityPlayer
        self.spawn_player()

        # Enemies --
        self.spawn_enemies()

        # Super pacgums --
        for floor_corner in self.maze.floor_corners:
            self.pacgum_list.append(
                VEntitySuperPacGum(self.atlas, floor_corner)
            )

        # Pacgums --
        forbbiden = {*self.maze.floor_corners, self.player.center}

        for floor_sprite in self.maze.floors.sprites:
            if floor_sprite.position not in forbbiden:
                if random.choices([True, False], weights=[70, 30])[0]:
                    position = Vec2(*floor_sprite.position)
                    self.pacgum_list.append(
                        VEntityPacGum(self.atlas, position)
                    )

        self.time_last_super_pacgum_ms: float = 0.0
        self.duration_super_pacgum_secs: float = 10.0

        self.setup_done = True

    # TODO: Check that --
    def spawn_player(self) -> None:
        """
        Spawn/respawn the player

        Calls self.player.kill() beforehand, thus acting as a respawn
        """
        if self.player_list:
            self.player.kill()

        self.player = VEntityPlayer(
            self.atlas,
            self.maze.floor_center,
            self.maze.walls,
            self.gamestate,
        )
        self.player_list.append(self.player)

    # TODO: Move enemy or entity management (spawning, updating, etc...)
    # to a separate class?
    # I feel like this class is becoming too big and complex
    def spawn_enemies(self) -> None:
        """
        Spawn/respawn all enemies in the order defined by self.ENEMY_ORDER
        """
        for enemy_class in self.ENEMY_ORDER:
            self.spawn_enemy(enemy_class)

    # ########################################################################
    # ##################################################### SPAWN ENEMIES ####
    def spawn_enemy(self, enemy_variant: EnemyVariantClass) -> None:
        """
        Spawn/respawn an enemy of the given variant
        """

        # Store the spawn positions for each enemy variant in a dictionary
        ENEMY_SPAWN_POSITIONS: dict[EnemyVariantClass, Vec2] = dict()
        for corner, enemy_class in zip(
            self.maze.floor_corners, self.ENEMY_ORDER
        ):
            ENEMY_SPAWN_POSITIONS[enemy_class] = corner

        # Get the existing enemy of the given variant, if any, and kill it
        enemy = next(
            (
                enemy
                for enemy in self.enemy_list
                if type(enemy) is enemy_variant
            ),
            None,
        )
        if enemy:
            enemy.kill()

        # Instantiate a new enemy
        spawn_position = ENEMY_SPAWN_POSITIONS[enemy_variant]
        new_enemy = enemy_variant(
            position=spawn_position,
            atlas=self.atlas,
            maze=self.maze,
            player=self.player,
            gamestate=self.gamestate,
        )
        # This is self-explanatory but it felt empty without this comment
        self.enemy_list.append(new_enemy)

    # ########################################################################
    # ########################################################### ON SHOW ####
    def on_show_view(self) -> None:
        # NOTE: We have to think about the setup and the process
        #       Check the subject page 7 about the game loop

        # self.setup()
        self.cameras_update()

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        if self.setup_done:
            self.cameras_update()

    # ########################################################################
    # ########################################################## NEW MAZE ####
    def new_maze(self, raw_width: int, raw_height: int, seed: int) -> None:
        maze_gen = MazeGeneratorWrapper()
        maze_gen.generate_new_maze(raw_width, raw_height, seed)
        self.maze = Maze(self.atlas, maze_gen.raw_maze)
        self.maze.build_sprites()
        self.maze.build_floor_graph()
        # print(self.maze.graph)

    # ########################################################################
    # #################################################### RELOAD SPRITES ####
    def reload_maze_sprites(self) -> None:
        # TODO: REWRITE IF NEEDED
        pass

        # self.walls.reload(
        #     self.maze_gen.walls.union(self.maze_gen.forty_two),
        #     self.maze_gen.floors,
        # )
        # self.floors.reload(self.maze_gen.floors)
        # self.cameras_update()

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        if self.setup_done:
            self.clear()
            with self.camera.activate():
                self.background.draw()
                self.maze.draw()
                self.pacgum_list.draw(pixelated=True)
                self.draw_enemy_paths()
                self.player_list.draw(pixelated=True)
                self.enemy_list.draw(pixelated=True)
                self.draw_hitboxes()

            with self.camera_hud.activate():
                self.hud.draw()

    # ########################################################################
    # ############################################# DRAW HITBOXES & PATHS ####
    def draw_hitboxes(self) -> None:
        if self.display_hitboxes:
            self.maze.walls.sprites.draw_hit_boxes(arcade.color.RED, 2)
            self.pacgum_list.draw_hit_boxes(arcade.color.WHITE, 1)
            self.player_list.draw_hit_boxes(arcade.color.GRANNY_SMITH_APPLE, 2)
            self.enemy_list.draw_hit_boxes(arcade.color.AFRICAN_VIOLET, 2)

    def draw_enemy_paths(self) -> None:
        if self.display_enemy_paths:
            line_width = VData.SPRITE_SIZE // 1.8
            if self.display_enemy_paths:
                for val, enemy in enumerate(self.enemy_list):
                    arcade.draw_line_strip(
                        enemy.bfs.path,
                        Color(val * 30, val * 50, val * 80),
                        line_width,
                    )
                    line_width -= 4

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        if self.setup_done and self.process_updates:
            self.handle_player_death()
            self.handle_super_pacgum_duration()

            self.maze.update(delta_time)
            self.background.update(delta_time)
            self.enemy_list.update(delta_time)  # type: ignore
            self.player_list.update(delta_time)  # type: ignore
            self.resolve_player_pacgum_collisions()
            self.resolve_player_enemy_collisions()

            self.enemy_list.update_animation(delta_time)  # type: ignore
            self.player_list.update_animation(delta_time)  # type: ignore
            self.pacgum_list.update_animation(delta_time)  # type: ignore

            self.hud.update(delta_time)

            self.gamestate.update(delta_time)

    # ########################################################################
    # ###################################################### PLAYER DEATH ####
    def is_player_dead(self) -> bool:
        return self.player not in self.player_list

    def handle_player_death(self) -> None:
        if self.is_player_dead():
            self.gamestate.decrement_lives()

            if self.gamestate.is_game_over:
                self.window.switch_view(VNames.VIEW_GAMEOVER)
            else:
                # QUESTION Why setup() here and not just continuing
                # QUESTION the current map ?
                # TODO: Use the spawning system to respawn the player and
                # the enemies instead of starting a new level
                self.setup()
                self.cameras_update()

    def handle_super_pacgum_duration(self) -> None:
        if (
            self.time_last_super_pacgum_ms + self.duration_super_pacgum_secs
            < time.time()
        ):
            self.gamestate.mode = GameState.Mode.CHASING

    # ########################################################################
    # ########################################## PLAYER PACGUM COLLISIONS ####
    def resolve_player_pacgum_collisions(self) -> None:
        collided: list[VEntityPacGum | VEntitySuperPacGum] = (
            arcade.check_for_collision_with_list(self.player, self.pacgum_list)
        )
        for pacgum in collided:
            self.gamestate.increment_score(pacgum.get_points())
            if isinstance(pacgum, VEntitySuperPacGum):
                self.time_last_super_pacgum_ms = time.time()
                self.gamestate.mode = GameState.Mode.FLEEING
            pacgum.kill()

    def resolve_player_enemy_collisions(self) -> None:
        # TODO: Clean that
        collided: list[VEntityEnemyCommon] = (
            arcade.check_for_collision_with_list(self.player, self.enemy_list)
        )
        if not collided:
            return
        if self.gamestate.mode == GameState.Mode.FLEEING:
            pass
        else:
            if not self.gamestate.cheats.god_mode:
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
                case arcade.key.R:
                    self.spawn_player()
                    self.spawn_enemies()

                case arcade.key.T:
                    self.test_bfs()

                case arcade.key.K:
                    self.window.switch_view(VNames.VIEW_GAMEOVER)

                case arcade.key.C:
                    self.window.switch_view(VNames.VIEW_CHEAT)

                # TODO: Potentially replace the current pause view with this
                # for pausing the game?
                # ANSWER: The subject explicitly requires a pause menu
                #         But it could be a cheat ?
                case arcade.key.SPACE:
                    self.process_updates = not self.process_updates

                case arcade.key.H:
                    self.display_hitboxes = not self.display_hitboxes
                    self.display_enemy_paths = not self.display_enemy_paths
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
                self.camera.position = self.maze.center_position

                self.camera_hud = arcade.Camera2D(hud_rect)
                self.camera_hud.position = self.hud.center_position

        def cameras_zoom() -> None:
            if self.setup_done:
                scale_hori = (
                    self.camera.viewport.width - VData.CAMERA_MARGIN
                ) / self.maze.width
                scale_vert = (
                    self.camera.viewport.height - VData.CAMERA_MARGIN
                ) / self.maze.height

                zoom = min(scale_hori, scale_vert)
                if zoom > VData.CAMERA_MAX_ZOOM:
                    zoom = VData.CAMERA_MAX_ZOOM

                self.camera.zoom = zoom
                self.camera_hud.zoom = zoom

        # --
        cameras_setup()
        cameras_zoom()

    # ########################################################################
    # ########################################################## TEST BFS ####
    def test_bfs(self) -> None:

        # Test from the player to the first enemy
        start = self.maze.closest_floor_of(self.player.center)
        target = self.maze.closest_floor_of(self.enemy_list[0].center)
        # start = target

        algo = BFS(self.maze.graph)
        algo.print_debug()

        algo.set_costs(start, target)
        algo.print_debug()

        algo.extract_path()
        algo.print_debug()
