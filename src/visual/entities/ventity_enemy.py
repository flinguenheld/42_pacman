from __future__ import annotations
from src.visual.entities.ventity_super_pacgum import VEntitySuperPacGum

from enum import Enum
from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vatlas import VAtlas
from src.visual.gamestate import GameState
from src.visual.pathfinding.bfs import BFS
from src.visual.pathfinding.fleeing import Fleeing
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.entities.ventity_player import VEntityPlayer, VPlayerDirection


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemyCommon(VEntityMoving):
    class Mode(Enum):
        CHASING = "chasing"
        FLEEING = "fleeing"
        DEAD = "dead"

    def __init__(
        self,
        corner_id: int,
        atlas: VAtlas,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        self.corner_id = corner_id
        self.texture_id = corner_id % atlas.nb_of_enemies

        super().__init__(
            atlas,
            f"enemy_{self.texture_id}_chasing",
            self.maze.floor_corners[corner_id],
        )

        self._mode = (
            VEntityEnemyCommon.Mode.CHASING,
            VEntityEnemyCommon.Mode.CHASING,
        )

        self.maze: Maze = maze
        self.player: VEntityPlayer = player
        self.gamestate: GameState = gamestate

        # --
        self.speed = self.gamestate.enemy_speed
        self.next_position: Vec2 = self.center
        self.bfs = BFS(self.maze.graph)
        self.fleeing = Fleeing(self.maze.graph)

        # Timers --
        self.timer_dead = 0.0
        self.timer_fleeing = 0.0

        # NOTE: I need that, as I want Michael and ReverseMichael to block
        # the player but not go straight for it if it stops moving.
        # TODO: Put that in player not here to perform update once ?
        self.last_player_direction: Vec2 = VPlayerDirection.UP.value

        self.update_next_position()

    # TODO: Clean that --
    def get_target(self) -> Vec2:
        raise NotImplementedError(
            "This method should be implemented in subclasses."
        )

    def update_last_player_direction(self) -> None:
        current_player_direction = self.player.get_direction_vector()
        if (
            current_player_direction != Vec2(0, 0)
            and current_player_direction != self.last_player_direction
        ):
            self.last_player_direction = current_player_direction

    # ########################################################################
    # ##################################################### NEXT POSITION ####
    def update_next_position(self) -> None:

        # QUESTION: Find a way to reduce the call of that method ?
        # QUESTION: Like only call after x times or when it has reached a pos ?

        start = self.maze.closest_floor_of(self.center)
        target = self.get_target()

        if self.next_position and start != self.next_position:
            return

        match self.current_mode:
            case VEntityEnemyCommon.Mode.CHASING:
                self.next_position = self.bfs.run_algo(start, target)
            case VEntityEnemyCommon.Mode.FLEEING:
                self.next_position = self.fleeing.run_algo(start, target)
            case VEntityEnemyCommon.Mode.DEAD:
                # TODO: Change that
                # TODO: Run the algo each time which is useless...

                self.next_position = self.bfs.run_algo(
                    start, self.maze.floor_corners[self.corner_id]
                )

    # ########################################################################
    # ########################################################## VELOCITY ####
    def update_velocity(self, delta_time: float) -> None:

        speed = self.apply_delta_time(self.speed, delta_time)
        next_position_delta = (self.next_position - self.center).normalize()

        # Change x/y are used by update_texture() --
        self.change_x = next_position_delta.x * speed * delta_time
        self.change_y = next_position_delta.y * speed * delta_time

        self.center_x += self.change_x
        self.center_y += self.change_y

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_last_player_direction()

        self.update_next_position()

        self.update_velocity(delta_time)
        self.update_texture()
        self.update_timers()

    # ########################################################################
    # ############################################################ TIMERS ####
    def update_timers(self, delta_time: float = 1 / 60) -> None:
        match self.current_mode:
            case VEntityEnemyCommon.Mode.FLEEING:
                self.timer_fleeing -= delta_time
                if self.timer_fleeing <= 0:
                    self.current_mode = VEntityEnemyCommon.Mode.CHASING

            case VEntityEnemyCommon.Mode.DEAD:
                self.timer_dead -= delta_time
                if self.timer_dead <= 0:
                    self.current_mode = VEntityEnemyCommon.Mode.CHASING

    # ########################################################################
    # ################################################### MODE PROPERTIES ####
    @property
    def previous_mode(self):
        return self._mode[0]

    @property
    def current_mode(self):
        return self._mode[1]

    @current_mode.setter
    def current_mode(self, new_mode: VEntityEnemyCommon.Mode):
        self._mode = (self._mode[1], new_mode)

        match new_mode:
            case VEntityEnemyCommon.Mode.CHASING:
                self._sprite_name = f"enemy_{self.texture_id}_chasing"
            case VEntityEnemyCommon.Mode.FLEEING:
                self._sprite_name = f"enemy_{self.texture_id}_fleeing"
                self.timer_fleeing = VEntitySuperPacGum.TIMER
            case VEntityEnemyCommon.Mode.DEAD:
                # TODO: Set the magic numbre somewhere ---
                # TODO: Set the magic numbre somewhere ---
                self._sprite_name = "enemy_dead"
                self.timer_dead = 10.0
