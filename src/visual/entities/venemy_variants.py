import arcade
from arcade import Sprite, Vec2

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gamestate import GameState
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_enemy import VEntityEnemyCommon


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
        gamestate: GameState,
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
        gamestate: GameState,
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
        gamestate: GameState,
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
        gamestate: GameState,
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
