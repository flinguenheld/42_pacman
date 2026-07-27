from __future__ import annotations

import arcade
from enum import Enum
from arcade import Sprite, Vec2, key

from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.gamestate import GameState
from src.visual.entities.ventity_moving import VEntityMoving


# ░░░░░░░░░█░█░█▀█░█░░░█▀█░█░█░█▀▀░█▀▄░░░█▀▄░▀█▀░█▀▄░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░▀▄▀░█▀▀░█░░░█▀█░░█░░█▀▀░█▀▄░░░█░█░░█░░█▀▄░█▀▀░█░░░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░▀░░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░░▀▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░
class VPlayerDirection(Enum):
    """
    Enum representing the possible movement directions for the player.
    """

    UP = Vec2(0, 1)
    LEFT = Vec2(-1, 0)
    DOWN = Vec2(0, -1)
    RIGHT = Vec2(1, 0)

    @staticmethod
    def return_direction_from_key(symbol: int) -> VPlayerDirection | None:
        """
        Takes a key as input and returns the corresponding player direction.
        If the key does not correspond to any direction, returns None.
        """
        match symbol:
            case key.UP | key.W | key.Z:
                return VPlayerDirection.UP
            case key.LEFT | key.A | key.Q:
                return VPlayerDirection.LEFT
            case key.DOWN | key.S:
                return VPlayerDirection.DOWN
            case key.RIGHT | key.D:
                return VPlayerDirection.RIGHT
            case _:
                return None


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀█░█░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░░░█▀█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
class VEntityPlayer(VEntityMoving):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        walls: SWall,
        gamestate: GameState,
    ) -> None:
        super().__init__(atlas, "player", position)
        self.walls: SWall = walls
        self.gamestate: GameState = gamestate

        self.current_directions: set[Vec2] = set()

        # QUESTION: Does the diagonal work with your keyboard ?

    # ########################################################################
    # ################################################## DIRECTION VECTOR ####
    def get_direction_vector(self) -> Vec2:
        """
        Returns the combined vector of all currently pressed directions.
        If no direction is pressed, returns a zero vector.
        Normalize the vector to ensure consistent speed in diagonal.
        """
        return sum(self.current_directions, Vec2(0, 0)).normalize()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_velocity(delta_time)
        self.update_texture()
        self.resolve_wall_collisions()

    # ########################################################################
    # ########################################################## VELOCITY ####
    def update_velocity(self, delta_time: float) -> None:
        """Update player movement based on pressed keys"""

        speed = self.apply_delta_time(self.gamestate.player_speed, delta_time)

        direction_vector = self.get_direction_vector()
        self.change_x = direction_vector.x * speed * delta_time
        self.change_y = direction_vector.y * speed * delta_time

    # ########################################################################
    # ######################################################## COLLISIONS ####
    def resolve_wall_collisions(self) -> None:
        # Resolve movement per-axis to avoid corner tunneling
        # and multi-wall phasing.
        self.center_x += self.change_x
        collided_x: list[Sprite] = arcade.check_for_collision_with_list(
            self, self.walls.sprites
        )
        if self.change_x > 0:
            for wall in collided_x:
                self.right = min(self.right, wall.left)
        elif self.change_x < 0:
            for wall in collided_x:
                self.left = max(self.left, wall.right)

        self.center_y += self.change_y
        collided_y: list[Sprite] = arcade.check_for_collision_with_list(
            self, self.walls.sprites
        )
        if self.change_y > 0:
            for wall in collided_y:
                self.top = min(self.top, wall.bottom)
        elif self.change_y < 0:
            for wall in collided_y:
                self.bottom = max(self.bottom, wall.top)

    # ########################################################################
    # ############################################################ ON KEY ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        direction = VPlayerDirection.return_direction_from_key(symbol)
        if direction is not None:
            self.current_directions.add(direction.value)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        direction = VPlayerDirection.return_direction_from_key(symbol)
        if direction is not None:
            self.current_directions.discard(direction.value)
