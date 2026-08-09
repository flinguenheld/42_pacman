from __future__ import annotations

from enum import Enum
from arcade import Vec2, key

from src.maze.maze import Maze
from src.sprites.vatlas import VAtlas
from src.data.gamestate import GameState
from src.entities.ventity_moving import VEntityMoving


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
        maze: Maze,
        gamestate: GameState,
    ) -> None:
        super().__init__(atlas, maze, "player", maze.floor_center)

        self.gamestate: GameState = gamestate
        self.directions_from_keys: set[Vec2] = set()
        self._alive: bool = True

    # ########################################################################
    # ############################################################# ALIVE ####
    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, value: bool) -> None:
        if self.gamestate.cheats.god_mode and not value:
            return
        self._alive = value

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_velocity(delta_time)
        self.update_position()
        self.update_texture()

    # ########################################################################
    # ################################################### UPDATE VELOCITY ####
    def update_velocity(self, delta_time: float) -> None:
        """Update player movement based on pressed keys."""

        speed = self.apply_delta_time(self.gamestate.player_speed, delta_time)
        direction = sum(self.directions_from_keys, Vec2(0, 0)).normalize()

        self.change_x = direction.x * speed * delta_time
        self.change_y = direction.y * speed * delta_time

    # ########################################################################
    # ################################################### UPDATE POSITION ####
    def update_position(self) -> None:
        """
        Update player position based on velocity.
        Check per axis, if the new position is in floors.
        Allow diagonal moves since they exist in the maze graph.

        If the player has moved in a new floor, update the maze graph.
        """

        # Cheat: No Clip --
        if self.gamestate.cheats.no_clip:
            # Did this to avoid bugs with the normal logic
            # and to keep the cheat logic separate.
            final_position = self.center + Vec2(self.change_x, self.change_y)
            if final_position != self.center:
                self.center = final_position
                self.current_floor = self.maze.closest_floor_of(self.center)
                self.maze.update_graph_values(self.current_floor)
            return

        def can_move_on(position: Vec2) -> bool:
            return (
                self.is_in_sprite(position, self.current_floor)
                or self.is_in_a_neighbour(position) is not None
            )

        final_position = self.center

        # Can move on x ? --
        if can_move_on(self.center + Vec2(self.change_x, 0)):
            final_position += Vec2(self.change_x, 0)
        else:
            self.change_x = 0  # Set 0 to avoid sprite update

        # Can move on y ? --
        if can_move_on(self.center + Vec2(0, self.change_y)):
            final_position += Vec2(0, self.change_y)
        else:
            self.change_y = 0

        # --
        if final_position != self.center:
            # Is still on current floor ? --
            if self.is_in_sprite(final_position, self.current_floor):
                self.center = final_position

            # Has moved to a new floor ? --
            next_floor = self.is_in_a_neighbour(final_position)
            if next_floor:
                self.center = final_position

                # Update the floor and the maze graph costs !!
                self.current_floor = next_floor
                self.maze.update_graph_values(self.current_floor)

    # ########################################################################
    # ############################################################ ON KEY ####
    def on_key_press(self, symbol: int) -> None:
        direction = VPlayerDirection.return_direction_from_key(symbol)
        if direction is not None:
            self.directions_from_keys.add(direction.value)

    def on_key_release(self, symbol: int) -> None:
        direction = VPlayerDirection.return_direction_from_key(symbol)
        if direction is not None:
            self.directions_from_keys.discard(direction.value)
