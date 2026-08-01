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

        super().__init__(
            atlas,
            maze,
            f"enemy_{self.texture_id}_{VEntityEnemyCommon.Mode.CHASING.value}",
            maze.floor_corners[corner_id],
        )

        self.player: VEntityPlayer = player
        self.gamestate: GameState = gamestate

        self.next_position: Vec2 = self.center
        self.speed = self.gamestate.enemy_speed
        self.mode = VEntityEnemyCommon.Mode.CHASING

        # Home mode --
        self.set_home_mode_triggers()

        # Timers --
        self.timer_dead = 0.0
        self.timer_fleeing = 0.0

    # ########################################################################
    # ############################################## HOME MODE - TRIGGERS ####
    def set_home_mode_triggers(self) -> None:
        """Set the triggers used in the home mode:
        - max_from_home: the enemy will come back near its start
        - max_from_player: if closer to player, it will continue to chase
        """

        # TODO: Overload this method to change their behaviours ?
        # TODO: Overload this method to change their behaviours ?

        value = max(self.maze.width, self.maze.height)
        value //= VData.SPRITE_SIZE

        self.max_from_home = int(value * 0.8)
        self.max_from_player = int(value * 0.4)

        print(f"trigger from home: {self.max_from_home}")
        print(f"trigger from player: {self.max_from_player}")

    # ########################################################################
    # ############################################ HOME MODE - MANAGEMENT ####
    def home_mode_management(self) -> None:
        """
        Get the distances from corner and from player.
        According to triggers, switch in home mode and move back to its corner.
        """

        current_floor = self.current_floor

        if self.current_floor in self.maze.graph_costs:
            from_home = self.maze.graph_corners[self.corner_id][current_floor]
            from_player = self.maze.graph_costs[current_floor]

            match self.mode:
                case VEntityEnemyCommon.Mode.CHASING:
                    if (
                        from_player > self.max_from_player
                        and from_home > self.max_from_home
                    ):
                        self.mode = VEntityEnemyCommon.Mode.HOME

                case VEntityEnemyCommon.Mode.HOME:
                    if from_home < 5 or from_player < self.max_from_player:
                        self.mode = VEntityEnemyCommon.Mode.CHASING

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
        to the current mode.
        """

        # Wait to be close to the next position before relaunching updating
        if self.center.distance(self.next_position) <= VData.SPRITE_SIZE / 10:
            self.home_mode_management()

            match self.mode:
                case VEntityEnemyCommon.Mode.CHASING:
                    self.next_position = self.maze.get_next_lowest(
                        self.current_floor
                    )

                case VEntityEnemyCommon.Mode.FLEEING:
                    self.next_position = self.maze.get_next_lowest(
                        self.current_floor,
                        reversed=True,
                    )

                case (
                    VEntityEnemyCommon.Mode.DEAD | VEntityEnemyCommon.Mode.HOME
                ):
                    self.next_position = self.maze.get_next_lowest(
                        self.current_floor,
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
        # print(f"     before new mode: {new_mode} -> {self.mode}")
        self._mode = new_mode
        print(f"     after new mode: {new_mode} -> {self.mode}")

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
