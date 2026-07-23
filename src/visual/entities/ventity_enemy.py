from enum import Enum, auto

import arcade
from arcade.types import Point2
from arcade import Sprite, Vec2

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.vgamestate import VGameState
from src.visual.sprites.sfloor import SFloor
from src.visual.pathfinding.astar import astar_search, random_path_search
from src.visual.pathfinding import PathfindingBarrierSet
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
        gamestate: VGameState,
    ) -> None:
        super().__init__(atlas, f"enemy_{id}", position)
        self.floors: SFloor = maze.floors
        self.walls: SWall = maze.walls
        self.player: VEntityPlayer = player
        self.gamestate: VGameState = gamestate
        self.maze: Maze = maze

        self.state: EnemyState = EnemyState.FLEEING

        self.path: list[Point2] | None = None
        self.next_position: Point2 | None = None
        self.next_sprite: Sprite | None = None
        self.last_goal: Point2 | None = None

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.dummy_target_sprite = Sprite()
        self.last_player_direction: Vec2 = VPlayerDirection.UP.get_vector()

        self.barrier_set = PathfindingBarrierSet(self.walls.sprites)
        self.update_closest_floor()
        self.update_next_position()

    def set_state(self, new_state: EnemyState) -> None:
        if self.state != new_state:
            self.state = new_state
            self.path = None
            self.next_position = None
            self.next_sprite = None
            self.last_goal = None

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> float:
        return self.gamestate.enemy_speed

    def get_target_sprite(self) -> Sprite:
        raise NotImplementedError(
            "This method should be implemented in subclasses."
        )

    def calculate_path(self) -> None:
        match self.state:
            case EnemyState.CHASING:
                target_sprite = self.get_target_sprite()

                start = self.closest_floor.position
                goal = target_sprite.position
                path = astar_search(start, goal, self.barrier_set)

                if not path:
                    self.path = None
                    self.last_goal = None
                    return
                self.path = path
                self.last_goal = target_sprite.position
            case EnemyState.FLEEING:
                start = self.closest_floor.position
                path = random_path_search(
                    start,
                    self.barrier_set,
                )
                if not path:
                    self.path = None
                    self.last_goal = None
                    return
                self.path = path
                self.last_goal = path[-1]
            case _:
                self.path = None
                self.last_goal = None
                return

    def should_recalculate_path(self) -> bool:
        # Generic checks
        if (
            self.next_position
            and self.next_position == self.closest_floor.position
        ):
            return False
        if not self.path or len(self.path) == 1 or not self.last_goal:
            return True

        # Reserved for CHASING state
        if self.state != EnemyState.CHASING:
            return False
        current_player_direction = self.player.get_direction_vector()
        if (
            current_player_direction != Vec2(0, 0)
            and current_player_direction != self.last_player_direction
        ):
            return True
        player_distance_to_last_goal = Vec2(*self.player.position).distance(
            Vec2(*self.last_goal)
        )
        distance_threshold = 3.0 * VData.SPRITE_SIZE
        if player_distance_to_last_goal > distance_threshold:
            return True
        return False

    def update_next_position(self) -> None:
        if self.should_recalculate_path():
            self.calculate_path()
        if not self.path:
            self.next_position = None
            self.next_sprite = None
            return
        if (
            not self.next_position
            or self.closest_floor.position == self.next_position
        ):
            self.path.pop(0)

            if len(self.path) > 0:
                self.next_position = self.path[0]
                sprites_at_next_pos = arcade.get_sprites_at_point(
                    self.next_position, self.floors.sprites
                )
                if sprites_at_next_pos:
                    self.next_sprite = sprites_at_next_pos[0]

    def update_closest_floor(self) -> Sprite | None:
        closest_floor = self.get_closest_sprite(self.floors.sprites)
        assert closest_floor, "Enemy is not on a floor tile."
        self.closest_floor = closest_floor
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


type EnemyVariant = type["Johnny | Michael | Charlie | ReverseMichael"]


class Johnny(VEntityEnemyCommon):
    """
    Johnny is a simple enemy that follows the player directly.
    Its goal is straightforward, it is to directly kill the player.

    Its target sprite is always the sprite the player is currently on.
    """

    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: VGameState,
    ) -> None:
        id = 0
        super().__init__(
            id,
            atlas,
            position,
            maze,
            player,
            gamestate,
        )

    def get_speed(self) -> float:
        return super().get_speed() * 0.9

    def get_target_sprite(self) -> Sprite:
        target_sprite = self.player.get_closest_sprite(self.floors.sprites)
        return target_sprite


class Michael(VEntityEnemyCommon):
    """
    Michael is a more advanced enemy that tries to predict the player's
    movement.
    He is more clever (or a coward, depending on how you see it) than Johnny,
    and will try to anticipate where the player is going.
    He won't try to kill the player directly, but will try to cut him off by
    predicting his next move.

    His target sprite is X tiles ahead of the player in the direction the
    player is currently moving.
    """

    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: VGameState,
    ) -> None:
        id = 1
        super().__init__(
            id,
            atlas,
            position,
            maze,
            player,
            gamestate,
        )

    def get_target_sprite(self) -> Sprite:
        player_direction = self.last_player_direction
        # 3 tiles ahead of the player
        distance_threshold = 3.0 * VData.SPRITE_SIZE
        target_pos = Vec2(*self.player.position) + (
            player_direction * distance_threshold
        )

        self.dummy_target_sprite.position = target_pos
        target_sprite_result = arcade.get_closest_sprite(
            self.dummy_target_sprite, self.floors.sprites
        )
        _error_msg = (
            "Could not find a closest sprite for "
            f"{self.dummy_target_sprite} in {self.floors.sprites}."
        )
        assert target_sprite_result is not None, _error_msg
        (target_sprite, _) = target_sprite_result

        return target_sprite


class Charlie(VEntityEnemyCommon):
    """
    Charlie is a creepy enemy that follows the player, but 3 seconds behind.
    He is faster than other ennemies, but a bit slower than the player,
    and will try to follow the player's movements,
    but with a delay of 3 seconds.
    """

    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: VGameState,
    ) -> None:
        id = 2
        self.player_movement_buffer: list[Vec2] = []
        self.max_buffer_size: int = int(3.0 * 60.0)  # 3 seconds at 60 FPS
        super().__init__(
            id,
            atlas,
            position,
            maze,
            player,
            gamestate,
        )

    def get_speed(self) -> float:
        # Charlie is slightly slower than the player
        return self.player.get_speed() * 0.5

    def update_player_movement_buffer(self) -> None:
        """
        Updates the player movement buffer with the player's current position.
        If the buffer has more than 3 seconds worth of positions, it pops the
        oldest position.
        """
        self.player_movement_buffer.append(Vec2(*self.player.position))
        if len(self.player_movement_buffer) > self.max_buffer_size:
            self.player_movement_buffer.pop(0)

    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_player_movement_buffer()
        return super().update(delta_time)

    def get_target_sprite(self) -> Sprite:
        if not self.player_movement_buffer:
            # If the buffer is empty, just return the player's
            # current position.
            target_pos = Vec2(*self.player.position)
        else:
            # Get the oldest position in the buffer, which is
            # probably 3 seconds behind.
            target_pos = self.player_movement_buffer[0]

        self.dummy_target_sprite.position = target_pos
        target_sprite_result = arcade.get_closest_sprite(
            self.dummy_target_sprite, self.floors.sprites
        )
        _error_msg = (
            "Could not find a closest sprite for "
            f"{self.dummy_target_sprite} in {self.floors.sprites}."
        )
        assert target_sprite_result is not None, _error_msg
        (target_sprite, _) = target_sprite_result

        return target_sprite


class ReverseMichael(VEntityEnemyCommon):
    """
    Michael is a more advanced enemy that tries to predict the player's
    movement.
    He is more clever (or a coward, depending on how you see it) than Johnny,
    and will try to anticipate where the player is going.
    He won't try to kill the player directly, but will try to cut him off by
    predicting his next move.

    His target sprite is X tiles ahead of the player in the direction the
    player is currently moving.
    """

    # TODO: Find a name for this enemy
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: VGameState,
    ) -> None:
        id = 3
        super().__init__(
            id,
            atlas,
            position,
            maze,
            player,
            gamestate,
        )

    def get_target_sprite(self) -> Sprite:
        player_direction = self.last_player_direction
        # 3 tiles ahead of the player
        distance_threshold = 3.0 * VData.SPRITE_SIZE
        target_pos = Vec2(*self.player.position) + (
            -player_direction * distance_threshold
        )

        self.dummy_target_sprite.position = target_pos
        target_sprite_result = arcade.get_closest_sprite(
            self.dummy_target_sprite, self.floors.sprites
        )
        _error_msg = (
            "Could not find a closest sprite for "
            f"{self.dummy_target_sprite} in {self.floors.sprites}."
        )
        assert target_sprite_result is not None, _error_msg
        (target_sprite, _) = target_sprite_result

        return target_sprite
