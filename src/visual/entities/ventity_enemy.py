from __future__ import annotations

from enum import Enum
from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.utils.usage import print_debug
from src.visual.pathfinding.patroling import Patroling
from src.visual.entities.ventity_moving import VEntityMoving


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemy(VEntityMoving):
    class Mode(Enum):
        CHASING = "chasing"
        FLEEING = "fleeing"
        PATROLING = "no texture"
        DEAD = "dead"

    def __init__(
        self,
        corner_id: int,
        atlas: VAtlas,
        maze: Maze,
        speed: int | float,
        patroling_trigger: int,
    ) -> None:
        self.corner_id = corner_id % len(maze.floor_corners)
        self.texture_id = self.corner_id % atlas.nb_of_enemies
        self.mode = VEntityEnemy.Mode.CHASING

        super().__init__(
            atlas,
            maze,
            f"enemy_{self.texture_id}_{self.mode.value}",
            maze.floor_corners[self.corner_id],
        )

        self.base_speed = speed
        self.next_position: Vec2 = self.center

        # Patroling mode --
        self.patroling_algo = Patroling(self.maze.graph_neighbours)
        self.patroling_trigger = patroling_trigger

        # Timers --
        self.timer_dead = 0.0
        self.timer_fleeing = 0.0

        # --
        print_debug(f"Enemy {self.corner_id} spawned:")
        print_debug(f"  -> speed {speed} - trigger {patroling_trigger}")

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
        if self.center.distance(self.next_position) <= VData.SPRITE_SIZE / 10:
            self.patroling_mode_management()

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
                case VEntityEnemy.Mode.PATROLING:
                    self.next_position = (
                        self.patroling_algo.next_random_positon(
                            self.current_floor
                        )
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

        next_floor = self.is_in_a_neighbour(self.center)
        if next_floor:
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
            case VEntityEnemy.Mode.CHASING:
                self._sprite_name = f"enemy_{self.texture_id}_{new_mode.value}"
            case VEntityEnemy.Mode.FLEEING:
                self._sprite_name = f"enemy_{self.texture_id}_{new_mode.value}"
                self.timer_fleeing = VData.TIMER_ENEMY_FLEEING
            case VEntityEnemy.Mode.DEAD:
                self._sprite_name = f"enemy_{new_mode.value}"
                self.timer_dead = VData.TIMER_ENEMY_DEATH
                self.update_texture(force=True)
            case _:
                pass

    # ########################################################################
    # ####################################### PATROLING MODE - MANAGEMENT ####
    def patroling_mode_management(self) -> None:
        """
        According to the distance to the player:
           - switch in patroling mode
           - come back to chasing mode
        """

        if self.current_floor in self.maze.graph_costs:
            from_player = self.maze.graph_costs[self.current_floor]

            match self.mode:
                case VEntityEnemy.Mode.CHASING:
                    if from_player > self.patroling_trigger:
                        self.mode = VEntityEnemy.Mode.PATROLING
                        print_debug(f"Enemy {self.corner_id} is patroling")
                case VEntityEnemy.Mode.PATROLING:
                    if from_player <= self.patroling_trigger:
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
            case VEntityEnemy.Mode.PATROLING:
                return self.base_speed * 0.8
            case VEntityEnemy.Mode.FLEEING:
                return self.base_speed * 1.1
            case VEntityEnemy.Mode.DEAD:
                return self.base_speed * 0.5
