from enum import Enum, auto

import arcade
from arcade import Sprite, Vec2, key

from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.vgamestate import VGameState


class VPlayerActions(Enum):
    """
    An enumeration of possible player actions,
    currently limited to movement directions.
    Acts as an abstraction layer between key inputs and game logic,
    allowing for multiple key bindings for the same action
    """

    MOVE_UP = auto()
    MOVE_LEFT = auto()
    MOVE_DOWN = auto()
    MOVE_RIGHT = auto()

    @staticmethod
    def return_action_from_key(symbol: int) -> "VPlayerActions | None":
        """
        Takes a key as input and returns the corresponding player action.
        If the key does not correspond to any action, returns None.
        """
        valid_keys: dict["VPlayerActions", list[int]] = {
            VPlayerActions.MOVE_UP: [key.UP, key.W, key.Z],
            VPlayerActions.MOVE_LEFT: [key.LEFT, key.A, key.Q],
            VPlayerActions.MOVE_DOWN: [key.DOWN, key.S],
            VPlayerActions.MOVE_RIGHT: [key.RIGHT, key.D],
        }
        for action, keys in valid_keys.items():
            if symbol in keys:
                return action
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
        gamestate: VGameState,
    ) -> None:
        super().__init__(atlas, "player", position)
        self.walls: SWall = walls
        self.gamestate: VGameState = gamestate
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.current_actions: set[VPlayerActions] = set()
        self.valid_keys: set[int] = {key.UP, key.DOWN, key.LEFT, key.RIGHT}

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

        speed = self.get_speed()

        self.change_x = 0
        self.change_y = 0

        if VPlayerActions.MOVE_UP in self.current_actions:
            self.change_y = speed * delta_time
        if VPlayerActions.MOVE_LEFT in self.current_actions:
            self.change_x = -speed * delta_time
        if VPlayerActions.MOVE_DOWN in self.current_actions:
            self.change_y = -speed * delta_time
        if VPlayerActions.MOVE_RIGHT in self.current_actions:
            self.change_x = speed * delta_time

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
        action = VPlayerActions.return_action_from_key(symbol)
        if action is not None:
            self.current_actions.add(action)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        action = VPlayerActions.return_action_from_key(symbol)
        if action is not None:
            self.current_actions.discard(action)
