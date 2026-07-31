from __future__ import annotations

from enum import Enum
from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gamestate import GameState
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.entities.ventity_player import VEntityPlayer


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
            f"enemy_{self.texture_id}_{VEntityEnemyCommon.Mode.CHASING.value}",
            maze.floor_corners[corner_id],
        )

        self.maze: Maze = maze
        self.player: VEntityPlayer = player
        self.gamestate: GameState = gamestate

        self.next_position: Vec2 = self.center
        self.speed = self.gamestate.enemy_speed
        self.mode = VEntityEnemyCommon.Mode.CHASING

        # Timers --
        self.timer_dead = 0.0
        self.timer_fleeing = 0.0

        self.update_next_position()

    # TODO: Add a control to keep the enemy close to it's corner
    # TODO: Add a control to keep the enemy close to it's corner
    # TODO: Add a control to keep the enemy close to it's corner

    # ########################################################################
    # ######################################################## GET TARGET ####
    def get_target(self) -> Vec2:
        """Overloaded by variants to adjust their behaviours."""
        return self.maze.closest_floor_of(self.player.center)

    # ########################################################################
    # ##################################################### NEXT POSITION ####
    def update_next_position(self) -> None:
        """
        Get in the maze's graph the next position to move according
        to the current move.
        """

        # Wait to be close to the next position before relaunching updating
        if self.center.distance(self.next_position) <= VData.SPRITE_SIZE / 10:
            start = self.maze.closest_floor_of(self.center)
            # target = self.get_target()

            match self.mode:
                case VEntityEnemyCommon.Mode.CHASING:
                    self.next_position = self.maze.get_next_lowest(start)

                case VEntityEnemyCommon.Mode.FLEEING:
                    self.next_position = self.maze.get_next_lowest(
                        start,
                        reversed=True,
                    )

                case VEntityEnemyCommon.Mode.DEAD:
                    self.next_position = self.maze.get_next_lowest(
                        start,
                        corner=self.corner_id,
                    )

    # ########################################################################
    # ########################################################## VELOCITY ####
    def update_velocity(self, delta_time: float) -> None:

        # Stop the enemy, which will set the texture to wait
        if abs(self.next_position.distance(self.center)) < 1:
            self.change_x = 0
            self.change_y = 0

        else:
            speed = self.apply_delta_time(self.speed, delta_time)
            next_pos_delta = (self.next_position - self.center).normalize()

            # Change x/y are used by update_texture() --
            self.change_x = next_pos_delta.x * speed * delta_time
            self.change_y = next_pos_delta.y * speed * delta_time

            self.center_x += self.change_x
            self.center_y += self.change_y

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_next_position()
        self.update_velocity(delta_time)
        self.update_texture()
        self.update_timers()

    # ########################################################################
    # ############################################################ TIMERS ####
    def update_timers(self, delta_time: float = 1 / 60) -> None:
        match self.mode:
            case VEntityEnemyCommon.Mode.FLEEING:
                self.timer_fleeing -= delta_time
                if self.timer_fleeing <= 0:
                    self.mode = VEntityEnemyCommon.Mode.CHASING

            case VEntityEnemyCommon.Mode.DEAD:
                self.timer_dead -= delta_time
                if self.timer_dead <= 0:
                    self.mode = VEntityEnemyCommon.Mode.CHASING

    # ########################################################################
    # ################################################### MODE PROPERTIES ####
    @property
    def mode(self) -> VEntityEnemyCommon.Mode:
        return self._mode

    @mode.setter
    def mode(self, new_mode: VEntityEnemyCommon.Mode) -> None:
        self._mode = new_mode

        match new_mode:
            case VEntityEnemyCommon.Mode.CHASING:
                self._sprite_name = f"enemy_{self.texture_id}_{new_mode.value}"
            case VEntityEnemyCommon.Mode.FLEEING:
                self._sprite_name = f"enemy_{self.texture_id}_{new_mode.value}"
                self.timer_fleeing = VData.TIMER_ENEMY_FLEEING
            case VEntityEnemyCommon.Mode.DEAD:
                self._sprite_name = f"enemy_{new_mode.value}"
                self.update_texture(True)
                self.timer_dead = VData.TIMER_ENEMY_DEATH
