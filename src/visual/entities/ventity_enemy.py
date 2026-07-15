from arcade import AStarBarrierList, Sprite, Vec2
import arcade

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.vgamestate import VGameState
from src.visual.sprites.sfloor import SFloor
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_moving import VEntityMoving


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemy(VEntityMoving):
    def __init__(
        self,
        id: int,
        atlas: VAtlas,
        position: Vec2,
        floors: SFloor,
        walls: SWall,
        player: VEntityPlayer,
        gamestate: VGameState,
        maze_gen: Maze,
    ) -> None:
        super().__init__(atlas, f"enemy_{id}", position)
        self.floors: SFloor = floors
        self.walls: SWall = walls
        self.player: VEntityPlayer = player
        self.gamestate: VGameState = gamestate
        self.maze_gen: Maze = maze_gen

        self.next_position: Vec2 | None = None
        self.next_sprite: arcade.Sprite | None = None
        self.path: list[tuple[float, float]] | None = None
        self.closest_floor: Sprite | None = None
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.update_closest_floor()
        self.setup_barrier_list()
        self.update_next_position()

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.enemy_speed

    def distance_to_player(self) -> float:
        return self.distance_to_entity(self.player)

    def setup_barrier_list(self) -> None:
        self.barrier_list = AStarBarrierList(
            self,
            self.walls.sprites,
            VData.SPRITE_SIZE,
            self.maze_gen.left,
            self.maze_gen.right,
            self.maze_gen.bot,
            self.maze_gen.top,
        )

    def compute_path(self) -> None:
        closest_player_floor = self.player.get_closest_sprite(
            self.floors.sprites
        )
        if not closest_player_floor:
            self.path = None
            return
        closest_floor = self.closest_floor
        if not closest_floor:
            self.path = None
            return
        path = arcade.astar_calculate_path(
            closest_floor.position,
            closest_player_floor.position,
            self.barrier_list,
            diagonal_movement=False,
        )
        self.path = path[1:] if path else None

    def update_next_position(self) -> None:
        if not self.path or len(self.path) < 2:
            self.compute_path()
        if not self.path:
            self.next_position = None
            self.next_sprite = None
            return
        closest_floor = self.closest_floor
        if not closest_floor or not self.path:
            self.next_position = None
            self.next_sprite = None
            return
        if (
            not self.next_position
            or closest_floor.position == self.next_position
        ):
            self.path.pop(0)

            if len(self.path) > 0:
                self.next_position = Vec2(*self.path[0])
                sprites_at_next_pos = arcade.get_sprites_at_point(
                    self.next_position, self.floors.sprites
                )
                if sprites_at_next_pos:
                    self.next_sprite = sprites_at_next_pos[0]

    def update_closest_floor(self) -> Sprite | None:
        self.closest_floor = self.get_closest_sprite(self.floors.sprites)
        return self.closest_floor

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        if not self.update_closest_floor():
            return
        self.update_next_position()

        self.update_velocity(delta_time)

        self.apply_velocity()
        self.update_texture()

    def update_velocity(self, delta_time: float) -> None:
        if not self.next_position:
            self.change_x = 0
            self.change_y = 0
            return

        speed = self.apply_delta_time(self.get_speed(), delta_time)

        next_position_delta = self.next_position - self.position
        next_position_normalized = next_position_delta.normalize()

        self.change_x = next_position_normalized.x * speed * delta_time
        self.change_y = next_position_normalized.y * speed * delta_time

    def apply_velocity(self) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
