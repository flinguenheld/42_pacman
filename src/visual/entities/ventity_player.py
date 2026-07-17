from enum import Enum, auto

import arcade
from arcade import Sprite, Vec2, key

from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.vgamestate import VGameState


class VPlayerDirections(Enum):
    """
    Enum representing the possible movement directions for the player.
    """

    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()

    @staticmethod
    def return_action_from_key(symbol: int) -> "VPlayerDirections | None":
        """
        Takes a key as input and returns the corresponding player direction.
        If the key does not correspond to any direction, returns None.
        """
        valid_keys: dict["VPlayerDirections", list[int]] = {
            VPlayerDirections.UP: [key.UP, key.W, key.Z],
            VPlayerDirections.LEFT: [key.LEFT, key.A, key.Q],
            VPlayerDirections.DOWN: [key.DOWN, key.S],
            VPlayerDirections.RIGHT: [key.RIGHT, key.D],
        }
        for direction, keys in valid_keys.items():
            if symbol in keys:
                return direction
        return None

    def get_vector(self) -> Vec2:
        """
        Returns the vector representation of the direction.
        """
        match self:
            case VPlayerDirections.UP:
                return Vec2(0, 1)
            case VPlayerDirections.LEFT:
                return Vec2(-1, 0)
            case VPlayerDirections.DOWN:
                return Vec2(0, -1)
            case VPlayerDirections.RIGHT:
                return Vec2(1, 0)


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀█░█░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░░░█▀█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
class VEntityPlayer(VEntityMoving):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        walls: SWall,
        gamestate: VGameState,
    ) -> None:
        super().__init__(atlas, "player", position)
        self.walls: SWall = walls
        self.gamestate: VGameState = gamestate
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.current_directions: set[VPlayerDirections] = set()
        self.valid_keys: set[int] = {key.UP, key.DOWN, key.LEFT, key.RIGHT}

    def get_direction_vector(self) -> Vec2:
        """
        Returns the combined vector of all currently pressed directions.
        If no direction is pressed, returns a zero vector.
        """
        if not self.current_directions:
            return Vec2(0, 0)

        combined_vector = Vec2(0, 0)
        for direction in self.current_directions:
            combined_vector += direction.get_vector()

        # Normalize the vector to ensure consistent speed in diagonal movement
        if combined_vector.length() > 0:
            combined_vector = combined_vector.normalize()

        return combined_vector

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.player_speed

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

        speed = self.apply_delta_time(self.get_speed(), delta_time)

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
        direction = VPlayerDirections.return_action_from_key(symbol)
        if direction is not None:
            self.current_directions.add(direction)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        direction = VPlayerDirections.return_action_from_key(symbol)
        if direction is not None:
            self.current_directions.discard(direction)
