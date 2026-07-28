from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vatlas import VAtlas
from src.visual.gamestate import GameState
from src.visual.pathfinding.bfs import BFS
from src.visual.pathfinding.fleeing import Fleeing
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.entities.ventity_player import VEntityPlayer


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemyCommon(VEntityMoving):
    def __init__(
        self,
        id: int,
        atlas: VAtlas,
        maze: Maze,
        player: VEntityPlayer,
        gamestate: GameState,
    ) -> None:
        super().__init__(
            atlas, f"enemy_{id}_chasing", position=maze.floor_corners[id]
        )

        # Keep the sprite name & mode to easily switch
        self.BASENAME = f"enemy_{id}"
        self.current_mode = GameState.Mode.CHASING

        self.maze: Maze = maze
        self.player: VEntityPlayer = player
        self.gamestate: GameState = gamestate

        # --
        self.speed = self.gamestate.enemy_speed
        self.next_position: Vec2 = self.center
        self.bfs = BFS(self.maze.graph)
        self.fleeing = Fleeing(self.maze.graph)

        self.update_next_position()

    # TODO: Clean that --
    def get_target(self) -> Vec2:
        raise NotImplementedError(
            "This method should be implemented in subclasses."
        )

    # ########################################################################
    # ######################################################## CHECK MODE ####
    def update_game_mode(self) -> None:
        """Switch the sprite_name according to the currnt gamestate"""
        # QUESTION: GOOD IDEA ????
        # IDEA: We could adapt their speed ??

        if self.current_mode != self.gamestate.mode:
            self._sprite_name = f"{self.BASENAME}_{self.gamestate.mode.value}"
            self.current_mode = self.gamestate.mode

    # ########################################################################
    # ##################################################### NEXT POSITION ####
    def update_next_position(self) -> None:

        # QUESTION: Find a way to reduce the call of that method ?
        # QUESTION: Like only call after x times or when it has reached a pos ?

        start = self.maze.closest_floor_of(self.center)
        target = self.get_target()

        if self.next_position and start != self.next_position:
            return

        match self.gamestate.mode:
            case GameState.Mode.CHASING:
                self.next_position = self.bfs.run_algo(start, target)
            case GameState.Mode.FLEEING:
                self.next_position = self.fleeing.run_algo(start, target)

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
        self.update_game_mode()
        self.update_next_position()
        self.update_velocity(delta_time)
        self.update_texture()
