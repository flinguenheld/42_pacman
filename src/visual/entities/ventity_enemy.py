from __future__ import annotations
import random

from enum import Enum
from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.utils.usage import print_debug
from src.visual.gamestate import GameState
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.entities.ventity_player import VEntityPlayer


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemy(VEntityMoving):
    class Mode(Enum):
        CHASING = "chasing"
        FLEEING = "fleeing"
        HOME = "no texture"
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
        self.mode = VEntityEnemy.Mode.CHASING

        super().__init__(
            atlas,
            maze,
            f"enemy_{self.texture_id}_{self.mode.value}",
            maze.floor_corners[corner_id],
        )

        self.player: VEntityPlayer = player
        self.gamestate: GameState = gamestate

        self.next_position: Vec2 = self.center
        self.speed = self.gamestate.enemy_speed

        # Home mode --
        self.set_home_mode_triggers()

        # Timers --
        self.timer_dead = 0.0
        self.timer_fleeing = 0.0

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
            self.home_mode_management()

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
                case VEntityEnemy.Mode.DEAD | VEntityEnemy.Mode.HOME:
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
    def update_current_floor(self):
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
    # ############################################## HOME MODE - TRIGGERS ####
    # Home mode allows to limit the enemy in its corner.
    # (Otherwise they follow the player in a group -_-')

    def set_home_mode_triggers(self) -> None:
        """Set the triggers used in the home mode:
        - hmode_trig_to_home: the enemy will come back near its start
        - hmode_trig_to_player: if closer to player, it will continue to chase
        - hmode_go_home_up_to: no need to touch the center
        """

        # TODO: Not very cool -_-'
        # TODO: It would be great if the enemy has a kind of default path
        #       And turn in its area like a guard...

        manhattan_to_center = self.maze.center_position // VData.SPRITE_SIZE
        max_axis = int(max(manhattan_to_center.x, manhattan_to_center.y))

        self.hmode_trig_to_home = random.randint(
            int(max_axis * 0.8), int(max_axis * 1.8)
        )
        self.hmode_trig_to_player = random.randint(4, 8)
        self.hmode_go_home_up_to = random.randint(1, 5)

        print_debug(f"-- enemy: {self.corner_id}")
        print_debug(f"HM: manhattan to center: {manhattan_to_center}")
        print_debug(f"HM: max axis: {max_axis}")
        print_debug(f"HM: trigger from home: {self.hmode_trig_to_home}")
        print_debug(f"HM: trigger from player: {self.hmode_trig_to_player}")
        print_debug(f"HM: go home up to: {self.hmode_go_home_up_to}")

    # ########################################################################
    # ############################################ HOME MODE - MANAGEMENT ####
    def home_mode_management(self) -> None:
        """
        Get the distances from corner and from player.
        According to triggers, switch in home mode and move back to its corner.
        """

        if self.current_floor in self.maze.graph_costs:
            from_home = self.maze.graph_corners[self.corner_id][
                self.current_floor
            ]
            from_player = self.maze.graph_costs[self.current_floor]

            match self.mode:
                case VEntityEnemy.Mode.CHASING:
                    if (
                        from_player > self.hmode_trig_to_player
                        and from_home > self.hmode_trig_to_home
                    ):
                        self.mode = VEntityEnemy.Mode.HOME
                case VEntityEnemy.Mode.HOME:
                    if (
                        from_home < self.hmode_go_home_up_to
                        or from_player < self.hmode_trig_to_player
                    ):
                        self.mode = VEntityEnemy.Mode.CHASING
                case _:
                    pass
