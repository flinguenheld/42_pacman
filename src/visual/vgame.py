import random
import arcade
from arcade import SpriteList, Vec2, LBWH

from src.maze.maze import Maze
from src.visual.vatlas import VAtlas
from src.visual.gui.ghud import VHud
from src.visual.gamestate import GameState
from src.visual.gui.gbackground import GBackground
from src.visual.vdata import VNames, VData, DebugMode
from src.maze.maze_wrapper import MazeGeneratorWrapper
from src.visual.entities.ventity_enemy import VEntityEnemy
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_pacgum import VEntityPacGum
from src.visual.entities.ventity_super_pacgum import VEntitySuperPacGum


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░
class VGame(arcade.View):
    def __init__(self, atlas: VAtlas, gamestate: GameState) -> None:
        super().__init__()

        self.atlas = atlas
        self.setup_done = False

        self.process_updates = True

        self.camera = arcade.Camera2D()
        self.camera_hud = arcade.Camera2D()

        self.gamestate = gamestate
        self.cheats = gamestate.cheats
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        """Restart the game."""

        # TODO: Implement the logic when the level is done
        # TODO:   -> Call setup and level - 1

        self.setup_done = False

        # Maze --
        self.new_maze()

        # Background --
        self.background = GBackground(self.atlas)
        self.background.build(self.maze.center_position, self.maze.rect)
        arcade.set_background_color(self.atlas.get_color("background"))

        # HUD --
        self.hud = VHud(
            self.maze,
            self.atlas,
            self.gamestate,
        )

        # Init sprite lists first --
        self.enemy_list: SpriteList[VEntityEnemy] = arcade.SpriteList()
        self.player_list: SpriteList[VEntityPlayer] = arcade.SpriteList()
        self.pacgum_list: SpriteList[VEntityPacGum] = arcade.SpriteList()
        self.super_pacgum_list: SpriteList[VEntitySuperPacGum] = (
            arcade.SpriteList()
        )
        self.combined_pacgum_list: SpriteList[
            VEntityPacGum | VEntitySuperPacGum
        ] = arcade.SpriteList()
        self.spawn_entities()

        self.setup_done = True

    # ########################################################################
    # ################################################### PLAYER PROPERTY ####
    @property
    def player(self) -> VEntityPlayer:
        return self.player_list[0]

    # ########################################################################
    # ################################## SPAWN PLAYER / ENEMIES / PACGUMS ####
    def spawn_entities(self) -> None:
        self.spawn_player()
        self.spawn_enemies()
        self.spawn_pacgums()

    def spawn_player(self) -> None:
        self.player_list.clear()
        self.player_list.append(
            VEntityPlayer(
                self.atlas,
                self.maze,
                self.gamestate,
            )
        )

    def spawn_enemies(self) -> None:
        self.maze.clear_costs()
        self.enemy_list.clear()

        for id in range(4):
            self.enemy_list.append(
                VEntityEnemy(
                    corner_id=id,
                    atlas=self.atlas,
                    maze=self.maze,
                    speed=self.gamestate.enemy_speed,
                    patroling_trigger=self.gamestate.enemy_patroling_trigger,
                )
            )

    def spawn_pacgums(self) -> None:
        self.combined_pacgum_list.clear()
        self._spawn_normal_pacgums()
        self._spawn_super_pacgums()

        combined = self.combined_pacgum_list
        combined.extend(self.pacgum_list)
        combined.extend(self.super_pacgum_list)

    def _spawn_normal_pacgums(self) -> None:
        """
        Do not use it by itself, use spawn_pacgums() instead.
        """
        self.pacgum_list.clear()

        forbidden = {*self.maze.floor_corners, self.player.center}

        for floor_sprite in self.maze.floors.sprites:
            if floor_sprite.position not in forbidden:
                if random.choices([True, False], weights=[70, 30])[0]:
                    position = Vec2(*floor_sprite.position)
                    pacgum = VEntityPacGum(self.atlas, position)
                    self.pacgum_list.append(pacgum)

    def _spawn_super_pacgums(self) -> None:
        """
        Do not use it by itself, use spawn_pacgums() instead.
        """
        self.super_pacgum_list.clear()

        for floor_corner in self.maze.floor_corners:
            super_pacgum = VEntitySuperPacGum(self.atlas, floor_corner)
            self.super_pacgum_list.append(super_pacgum)

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
    def new_maze(self) -> None:
        def get_seed() -> int:
            if self.gamestate.level == 1:
                return 42
            else:
                return random.randint(1, 100000)

        seed = get_seed()
        raw_width = random.randint(10, 20)
        raw_height = random.randint(5, 15)
        maze_gen = MazeGeneratorWrapper()
        maze_gen.generate_new_maze(raw_width, raw_height, seed)
        print(
            "Generated new maze - "
            f"Seed: {seed}, Size: {raw_width}x{raw_height}"
        )
        self.maze = Maze(self.atlas, maze_gen.raw_maze)
        self.maze.build(include_graph=True)

    # ########################################################################
    # #################################################### RELOAD SPRITES ####
    def reload_maze_sprites(self) -> None:
        # TODO: Might need this function if we reimplement
        # the style switching feature
        pass

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        def draw_people() -> None:
            self.player_list.draw(pixelated=True)
            self.enemy_list.draw(pixelated=True)

        if self.setup_done:
            self.clear()
            with self.camera.activate():
                self.background.draw()
                self.maze.draw()

                match VData.debug_mode:
                    case DebugMode.HITBOXES:
                        self.combined_pacgum_list.draw(pixelated=True)
                        draw_people()
                        self.draw_hitboxes()
                    case DebugMode.ALGO:
                        draw_people()
                    case DebugMode.OFF:
                        self.combined_pacgum_list.draw(pixelated=True)
                        draw_people()

            with self.camera_hud.activate():
                self.hud.draw()

    # ########################################################################
    # ############################################# DRAW HITBOXES & PATHS ####
    def draw_hitboxes(self) -> None:
        self.combined_pacgum_list.draw_hit_boxes(arcade.color.BLUE_BELL, 2)
        self.player_list.draw_hit_boxes(arcade.color.GRANNY_SMITH_APPLE, 2)
        self.enemy_list.draw_hit_boxes(arcade.color.RED_DEVIL, 2)

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        if self.setup_done and self.process_updates:
            self.maze.update(delta_time)
            self.background.update(delta_time)
            self.enemy_list.update(delta_time)
            self.player_list.update(delta_time)
            self.pacgum_collisions()
            self.enemy_collisions()

            self.enemy_list.update_animation(delta_time)
            self.player_list.update_animation(delta_time)
            self.combined_pacgum_list.update_animation(delta_time)

            self.hud.update(delta_time)

            self.gamestate.update(delta_time)

    # ########################################################################
    # ######################################################## COLLISIONS ####
    def pacgum_collisions(self) -> None:
        for pacgum in arcade.check_for_collision_with_list(
            self.player,
            self.pacgum_list,
        ):
            self.gamestate.score += pacgum.get_points()
            pacgum.kill()

        for super_pacgum in arcade.check_for_collision_with_list(
            self.player, self.super_pacgum_list
        ):
            self.gamestate.score += super_pacgum.get_points()
            self.switch_all_enemies_to_fleeing()
            super_pacgum.kill()

        if len(self.combined_pacgum_list) == 0:
            self.go_to_next_level()

    def enemy_collisions(self) -> None:
        for enemy in arcade.check_for_collision_with_list(
            self.player, self.enemy_list
        ):
            match enemy.mode:
                case VEntityEnemy.Mode.CHASING:
                    if not self.cheats.god_mode:
                        self.player_death()
                case VEntityEnemy.Mode.FLEEING:
                    enemy.mode = VEntityEnemy.Mode.DEAD
                case _:
                    pass

    # ########################################################################
    # ###################################################### PLAYER DEATH ####
    def player_death(self) -> None:
        self.gamestate.decrement_lives()

        if self.gamestate.is_game_over:
            self.window.switch_view(VNames.VIEW_GAMEOVER)
        else:
            self.spawn_entities()
            self.cameras_update()

    def go_to_next_level(self) -> None:
        self.window.switch_view(VNames.VIEW_GAME_NEXT_LEVEL)

    # ########################################################################
    # ######################################### SWITCH ENEMIES TO FLEEING ####
    def switch_all_enemies_to_fleeing(self) -> None:
        for enemy in self.enemy_list:
            if enemy.mode != VEntityEnemy.Mode.DEAD:
                enemy.mode = VEntityEnemy.Mode.FLEEING

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Player movement is handled in the player class.
        # The WASD, ZQSD and arrow keys are reserved for player movement.

        if self.setup_done:
            match symbol:
                case arcade.key.ESCAPE:
                    self.window.switch_view(VNames.VIEW_PAUSE)

                case arcade.key.N:
                    self.setup()
                    self.cameras_update()
                case arcade.key.R:
                    self.spawn_entities()

                case arcade.key.SPACE:
                    self.process_updates = not self.process_updates

                case arcade.key.H:
                    VData.toggle_debug_mode()

                case _:
                    pass

            # TODO: reimplement style switching feature and change key
            # elif symbol == arcade.key.S:
            #     self.sprite_manager.next_style()
            #     self.sprite_manager.reload(self.maze_gen, reload_atlas=True)
            #     arcade.set_background_color(self.sprite_manager.background_color)

            self.player.on_key_press(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if self.setup_done:
            self.player.on_key_release(symbol)

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
