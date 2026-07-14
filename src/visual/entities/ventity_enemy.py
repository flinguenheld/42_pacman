from enum import Enum, auto

from arcade import AStarBarrierList, Vec2
import arcade

from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.vatlas import VAtlas
from src.visual.sprites.sfloor import SFloor
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.vdata import VData
from src.visual.vgamestate import VGameState


class EnemyDirection(Enum):
    NONE = 0
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


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

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.setup_barrier_list()
        self.compute_path()
        self.get_next_position()

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.enemy_speed

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
        closest_enemy_floor = self.get_closest_sprite(self.floors.sprites)
        if not closest_enemy_floor:
            self.path = None
            return
        path = arcade.astar_calculate_path(
            closest_enemy_floor.position,
            closest_player_floor.position,
            self.barrier_list,
            diagonal_movement=False,
        )
        self.path = path[1:] if path else None

    def get_next_position(self) -> None:
        if not self.path:
            self.compute_path()
        if not self.path:
            self.next_position = None
            self.next_sprite = None
            return
        closest_floor = self.get_closest_sprite(self.floors.sprites)
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
                sprites = arcade.get_sprites_at_point(
                    self.next_position, self.floors.sprites
                )
                if sprites:
                    self.next_sprite = sprites[0]

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.get_next_position()

        direction = EnemyDirection.NONE
        if self.next_position:
            next_position = self.next_position
            next_position_delta = next_position - self.position
            if abs(next_position_delta.x) > abs(next_position_delta.y):
                if next_position_delta.x > 0:
                    direction = EnemyDirection.RIGHT
                else:
                    direction = EnemyDirection.LEFT
            else:
                if next_position_delta.y > 0:
                    direction = EnemyDirection.UP
                else:
                    direction = EnemyDirection.DOWN
        else:
            direction = EnemyDirection.NONE

        speed = self.get_speed()

        self.change_x = 0
        self.change_y = 0

        match direction:
            case EnemyDirection.UP:
                self.change_y = speed * delta_time
            case EnemyDirection.LEFT:
                self.change_x = -speed * delta_time
            case EnemyDirection.DOWN:
                self.change_y = -speed * delta_time
            case EnemyDirection.RIGHT:
                self.change_x = speed * delta_time
            case EnemyDirection.NONE:
                pass

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.update_texture()
