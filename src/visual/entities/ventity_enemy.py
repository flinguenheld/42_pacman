from enum import Enum, auto

from arcade.types import Point2
from arcade import Sprite, Vec2

from src.maze.maze import Maze
from src.visual.pathfinding.bfs import BFS
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.gamestate import GameState
from src.visual.sprites.sfloor import SFloor
from src.visual.pathfinding.astar import random_path_search
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.entities.ventity_player import VEntityPlayer, VPlayerDirection


class EnemyState(Enum):
    """
    Enum for the different states an enemy can be in.
    """

    CHASING = auto()
    FLEEING = auto()
    DEAD = auto()


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemyCommon(VEntityMoving):
    def __init__(
        self,
        id: int,
        atlas: VAtlas,
        position: Vec2,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        super().__init__(atlas, f"enemy_{id}", position)
        self.floors: SFloor = maze.floors
        self.walls: SWall = maze.walls
        self.player: VEntityPlayer = player
        self.gamestate: GameState = gamestate
        self.maze: Maze = maze

        self.state: EnemyState = EnemyState.CHASING

        self.next_position: Point2 | None = None

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.dummy_target_sprite = Sprite()
        self.last_player_direction: Vec2 = VPlayerDirection.UP.get_vector()

        self.bfs = BFS(self.maze.graph)
        self.update_next_position()

    def set_state(self, new_state: EnemyState) -> None:
        if self.state != new_state:
            self.state = new_state

    @staticmethod
    def get_points() -> int:
        return VData.points_per_ghost

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> float:
        return self.gamestate.enemy_speed

    def get_target(self) -> Vec2:
        raise NotImplementedError(
            "This method should be implemented in subclasses."
        )

    def update_next_position(self) -> None:
        # TODO: Update method to use closest_floor_of if possible
        # TODO: Update method to return Vec2 instead of Sprite
        start = self.maze.closest_floor_of(self.center)
        target = self.get_target()

        if self.next_position and start != self.next_position:
            return

        def next_pos_chasing() -> Vec2 | None:
            return self.bfs.run(start, target)

        def next_pos_fleeing() -> Vec2 | None:
            path = random_path_search(start, self.maze.graph)
            return Vec2(*path[1]) if len(path) > 1 else None

        match self.state:
            case EnemyState.CHASING:
                self.next_position = next_pos_chasing()
            case EnemyState.FLEEING:
                self.next_position = next_pos_fleeing()
            case _:
                self.next_position = None

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_next_position()

        self.update_velocity(delta_time)

        self.apply_velocity()
        self.update_texture()
        self.update_last_player_direction()

    def update_velocity(self, delta_time: float) -> None:
        if not self.next_position:
            self.change_x = 0
            self.change_y = 0
            return

        speed = self.apply_delta_time(self.get_speed(), delta_time)

        next_position_delta = Vec2(*self.next_position) - Vec2(*self.position)
        next_position_normalized = next_position_delta.normalize()

        self.change_x = next_position_normalized.x * speed * delta_time
        self.change_y = next_position_normalized.y * speed * delta_time

    def apply_velocity(self) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_last_player_direction(self) -> None:
        player_direction_vector = self.player.get_direction_vector()
        if player_direction_vector != Vec2(0, 0):
            self.last_player_direction = player_direction_vector
