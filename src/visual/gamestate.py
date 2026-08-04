from enum import Enum
from src.visual.vdata import VData


# QUESTION: cheats is in game states and game state is in cheats :|
class Cheats:
    def __init__(self, game_state: "GameState") -> None:
        self.game_state = game_state

        self.god_mode: bool = False
        self.no_clip: bool = False

    def toggle_god_mode(self) -> None:
        self.god_mode = not self.god_mode

    def toggle_no_clip(self) -> None:
        self.no_clip = not self.no_clip

    def update_lives(self, lives: int) -> None:
        self.game_state.lives = lives


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▄█░█▀▀░█▀▀░▀█▀░█▀█░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█░█░█▀▀░▀▀█░░█░░█▀█░░█░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀░▀░░▀░░▀▀▀░░
class GameState:
    class Mode(Enum):
        CHASING = "chasing"
        FLEEING = "fleeing"

    def __init__(self) -> None:
        # TODO: These values have to be set with the config
        self.score: int = 0
        self.lives: int = 3
        self.timer = VData.time_max

        self._player_speed: float = 30.0
        self._enemy_speed: float = 15.0

        self.mode: GameState.Mode = GameState.Mode.CHASING

        self.cheats: Cheats = Cheats(self)

    # ########################################################################
    # ##################################################### SCORE & LIVES ####
    def increment_score(self, points: int) -> None:
        self.score += points

    def decrement_lives(self) -> None:
        if self.lives > 0:
            self.lives -= 1

    # ########################################################################
    # ######################################################### GAME OVER ####
    @property
    def is_game_over(self) -> bool:
        return self.timer <= 0 or self.lives <= 0

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.timer -= delta_time

    # ########################################################################
    # ############################################################# SPEED ####
    # QUESTION Useful here ?
    @property
    def player_speed(self) -> float:
        return self._player_speed

    @property
    def enemy_speed(self) -> float:
        return self._enemy_speed
