from arcade import Sprite, Vec2
import arcade
from arcade.types import Point2

from src.visual.pathfinding import PathfindingAlgorithm
from src.visual.pathfinding.astar import AStarSearch
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.vgamestate import VGameState
from src.visual.sprites.sfloor import SFloor
from src.visual.entities.ventity_player import VEntityPlayer, VPlayerDirections
from src.visual.entities.ventity_moving import VEntityMoving


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemyCommon(VEntityMoving):
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

        self.pathfinder: type[PathfindingAlgorithm] = AStarSearch

        self.path: list[Point2] | None = None
        self.next_position: Point2 | None = None
        self.next_sprite: Sprite | None = None
        self.target_sprite: Sprite | None = None
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.dummy_target_sprite = Sprite()
        self.last_player_direction: Vec2 = VPlayerDirections.UP.get_vector()

        self.update_closest_floor()
        self.update_next_position()

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> float:
        return self.gamestate.enemy_speed

    def get_target_sprite(self) -> Sprite:
        raise NotImplementedError(
            "This method should be implemented in subclasses."
        )

    def calculate_path(self) -> None:
        self.target_sprite = self.get_target_sprite()

        start = self.closest_floor.position
        goal = self.target_sprite.position
        path = self.pathfinder(
            start=start,
            goal=goal,
            blocked_sprites=self.walls.sprites,
        ).calculate_path()

        if not path:
            self.path = None
            self.target_sprite = None
            return
        self.path = path

    def should_recompute_path(self) -> bool:
        if (
            self.next_position
            and self.next_position == self.closest_floor.position
        ):
            return False
        if not self.path or len(self.path) < 2 or not self.target_sprite:
            return True
        distance_to_player_from_target_sprite = (
            arcade.get_distance_between_sprites(
                self.target_sprite, self.player
            )
        )
        if distance_to_player_from_target_sprite > (1.0 * VData.SPRITE_SIZE):
            return True
        return False

    def update_next_position(self) -> None:
        if self.should_recompute_path():
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
        floors: SFloor,
        walls: SWall,
        player: VEntityPlayer,
        gamestate: VGameState,
        maze_gen: Maze,
    ) -> None:
        id = 0
        super().__init__(
            id,
            atlas,
            position,
            floors,
            walls,
            player,
            gamestate,
            maze_gen,
        )

    def get_target_sprite(self) -> Sprite:
        target_sprite_result = self.player.get_closest_sprite(
            self.floors.sprites
        )
        return target_sprite_result


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
        floors: SFloor,
        walls: SWall,
        player: VEntityPlayer,
        gamestate: VGameState,
        maze_gen: Maze,
    ) -> None:
        id = 1

        super().__init__(
            id,
            atlas,
            position,
            floors,
            walls,
            player,
            gamestate,
            maze_gen,
        )

    def get_target_sprite(self) -> Sprite:
        dir = self.player.get_direction_vector()
        if dir == Vec2(0, 0):
            dir = self.last_player_direction
        else:
            self.last_player_direction = dir
        target_pos = self.player.position + (dir * 3.0 * VData.SPRITE_SIZE)

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


type EnemyVariant = type[Johnny | Michael]
