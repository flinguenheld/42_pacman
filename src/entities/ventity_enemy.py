from __future__ import annotations

from enum import Enum
from arcade import Vec2

from src.maze.maze import Maze
from src.config.config import Config
from src.sprites.vatlas import VAtlas
from src.utils.utils import print_debug
from src.pathfinding.patrolling import Patrolling
from src.entities.ventity_moving import VEntityMoving


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemy(VEntityMoving):
    class Mode(Enum):
        CHASING = "chasing"
        FLEEING = "fleeing"
        PATROLLING = "patrolling"
        DEAD = "dead"

    def __init__(
        self,
        corner_id: int,
        atlas: VAtlas,
        maze: Maze,
        speed: int | float,
        patrolling_trigger: int,
    ) -> None:
        self._mode = VEntityEnemy.Mode.CHASING
        self.corner_id = corner_id % len(maze.floor_corners)
        self.texture_id = self.corner_id % atlas.nb_of_enemies
        self.affected_corner = maze.floor_corners[self.corner_id]

        super().__init__(
            atlas,
            maze,
            f"enemy_{self.texture_id}_{self._mode.value}",
            self.affected_corner,
        )

        self.base_speed = speed
        self.next_position: Vec2 = self.center

        # Patrolling mode --
        self.patrolling_algo = Patrolling(self.maze, self.corner_id)
        self.patrolling_trigger = patrolling_trigger

        # Timers --
        self.timer_dead = 0.0
        self.timer_fleeing = 0.0

        # --
        print_debug(f"Enemy {self.corner_id} spawned:")
        print_debug(f"  -> speed {speed} - trigger {patrolling_trigger}")

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.get_next_position()
        self.update_velocity(delta_time)
        self.update_current_floor()
        self.update_texture()
        self.update_timers()

    # ########################################################################
    # ##################################################### NEXT POSITION ####
    def get_next_position(self) -> None:
        """
        Get in the maze's graph the next position to move according
        to the current mode.
        """

        # Wait to be close to the next position.
        if self.center.distance(self.next_position) <= Config.SPRITE_SIZE / 10:
            self.patrolling_mode_management()

            match self.mode:
                case VEntityEnemy.Mode.CHASING:
                    self.next_position = self.maze.get_next_lowest(
                        self.current_floor
                    )
                case VEntityEnemy.Mode.FLEEING:
                    self.next_position = self.maze.get_next_lowest(
                        self.current_floor,
                        reversed=True,
                    )
                case VEntityEnemy.Mode.PATROLLING:
                    self.next_position = self.patrolling_algo.next_position(
                        self.current_floor
                    )
                case VEntityEnemy.Mode.DEAD:
                    self.next_position = self.maze.get_next_lowest(
                        self.current_floor,
                        corner=self.corner_id,
                    )

    # ########################################################################
    # ################################################### UPDATE VELOCITY ####
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
    # ############################################## UPDATE CURRENT FLOOR ####
    def update_current_floor(self) -> None:
        """Update the current floor according to the position."""

        if next_floor := self.is_in_a_neighbour(self.center):
            self.current_floor = next_floor

    # ########################################################################
    # ############################################################ TIMERS ####
    def update_timers(self, delta_time: float = 1 / 60) -> None:
        match self.mode:
            case VEntityEnemy.Mode.FLEEING:
                self.timer_fleeing -= delta_time
                if self.timer_fleeing <= 0:
                    self.mode = VEntityEnemy.Mode.CHASING
            case VEntityEnemy.Mode.DEAD:
                if self.current_floor == self.affected_corner:
                    self.timer_dead -= delta_time
                    if self.timer_dead <= 0:
                        self.mode = VEntityEnemy.Mode.CHASING
            case _:
                pass

    # ########################################################################
    # ################################################### MODE PROPERTIES ####
    @property
    def mode(self) -> VEntityEnemy.Mode:
        return self._mode

    @mode.setter
    def mode(self, new_mode: VEntityEnemy.Mode) -> None:
        self._mode = new_mode
        match new_mode:
            case VEntityEnemy.Mode.PATROLLING | VEntityEnemy.Mode.CHASING:
                self._sprite_name = f"enemy_{self.texture_id}_{new_mode.value}"
            case VEntityEnemy.Mode.FLEEING:
                self._sprite_name = f"enemy_{self.texture_id}_{new_mode.value}"
                self.timer_fleeing = Config.timer_enemy_fleeing
            case VEntityEnemy.Mode.DEAD:
                self._sprite_name = f"enemy_{new_mode.value}"
                self.timer_dead = Config.timer_enemy_death

        self.update_texture(force=True)

    # ########################################################################
    # ###################################### PATROLLING MODE - MANAGEMENT ####
    def patrolling_mode_management(self) -> None:
        """
        According to the distance to the player:
           - switch in patrolling mode
           - come back to chasing mode
        """

        if self.current_floor in self.maze.graph_costs:
            from_player = self.maze.graph_costs[self.current_floor]

            match self.mode:
                case VEntityEnemy.Mode.CHASING:
                    if from_player > self.patrolling_trigger:
                        self.mode = VEntityEnemy.Mode.PATROLLING
                        print_debug(f"Enemy {self.corner_id} is patrolling")
                case VEntityEnemy.Mode.PATROLLING:
                    if from_player <= self.patrolling_trigger:
                        self.mode = VEntityEnemy.Mode.CHASING
                        print_debug(f"Enemy {self.corner_id} is chasing !!")
                case _:
                    pass

    # ########################################################################
    # ############################################################# SPEED ####
    @property
    def speed(self) -> float:
        """Get speed according to the current mode."""
        match self.mode:
            case VEntityEnemy.Mode.CHASING:
                return self.base_speed * 1.2
            case VEntityEnemy.Mode.PATROLLING:
                return self.base_speed * 0.8
            case VEntityEnemy.Mode.FLEEING:
                return self.base_speed * 1.1
            case VEntityEnemy.Mode.DEAD:
                return self.base_speed * 0.8
