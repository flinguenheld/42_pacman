from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vatlas import VAtlas
from src.visual.gamestate import GameState
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_enemy import VEntityEnemyCommon


type EnemyVariantClass = type["Johnny | Michael | Charlie | ReverseMichael"]
type EnemyVariant = "Johnny | Michael | Charlie | ReverseMichael"


class Johnny(VEntityEnemyCommon):
    """
    Johnny is a simple enemy that follows the player directly.
    Its goal is straightforward, it is to directly kill the player.

    Its target sprite is always the sprite the player is currently on.
    """

    def __init__(
        self,
        atlas: VAtlas,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        super().__init__(0, atlas, maze, player, gamestate)
        self.speed *= 0.9


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
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        super().__init__(1, atlas, maze, player, gamestate)

    # def get_target(self) -> Vec2:
    #     # TODO: To confirm
    #     if self.player.direction_previous != Vec2(0, 0):
    #         player_direction = self.player.direction_previous
    #     else:
    #         player_direction = self.player.direction_current

    #     distance_threshold = 3.0 * VData.SPRITE_SIZE
    #     possible = self.player.center + (player_direction * distance_threshold)

    #     return self.maze.closest_floor_of(possible)


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
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        self.player_movement_buffer: list[Vec2] = []
        self.max_buffer_size: int = int(3.0 * 60.0)  # 3 seconds at 60 FPS

        super().__init__(2, atlas, maze, player, gamestate)
        self.speed = self.gamestate.player_speed * 0.8

    # def update_player_movement_buffer(self) -> None:
    #     """
    #     Updates the player movement buffer with the player's current position.
    #     If the buffer has more than 3 seconds worth of positions, it pops the
    #     oldest position.
    #     """
    #     self.player_movement_buffer.append(Vec2(*self.player.position))
    #     if len(self.player_movement_buffer) > self.max_buffer_size:
    #         self.player_movement_buffer.pop(0)

    # def update(self, delta_time: float = 1 / 60) -> None:
    #     self.update_player_movement_buffer()
    #     return super().update(delta_time)

    # def get_target(self) -> Vec2:
    #     if not self.player_movement_buffer:
    #         # If the buffer is empty, just return the player's
    #         # current position.
    #         possible = Vec2(*self.player.position)
    #     else:
    #         # Get the oldest position in the buffer, which is
    #         # probably 3 seconds behind.
    #         possible = self.player_movement_buffer[0]

    #     return self.maze.closest_floor_of(possible)


class ReverseMichael(VEntityEnemyCommon):
    """
    ReverseMichael is a more advanced enemy that tries to predict the player's
    movement.
    He is more clever (or a coward, depending on how you see it) than Johnny,
    and will try to anticipate where the player is going.
    He won't try to kill the player directly, but will try to cut him off by
    predicting his next move.

    His target sprite is X tiles ahead of the player in the opposite direction
    the player is currently moving.
    """

    # TODO: Find a name for this enemy

    def __init__(
        self,
        atlas: VAtlas,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        super().__init__(3, atlas, maze, player, gamestate)

    # def get_target(self) -> Vec2:
    #     # TODO: To confirm
    #     if self.player.direction_previous != Vec2(0, 0):
    #         player_direction = self.player.direction_previous
    #     else:
    #         player_direction = self.player.direction_current

    #     distance_threshold = 3.0 * VData.SPRITE_SIZE
    #     possible = self.player.center + (
    #         -player_direction * distance_threshold
    #     )

    #     return self.maze.closest_floor_of(possible)
