from src.visual.vdata import VData

# QUESTION: Rename to GameState ?


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░█▀▀░▀█▀░█▀█░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░▀▀█░░█░░█▀█░░█░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀░▀░░▀░░▀▀▀░░
class VGameState:
    def __init__(self) -> None:
        # TODO: These values have to be set with the config
        self.score: int = 0
        self.lives: int = 3
        self.timer = VData.time_max

        self._player_speed: float = 30.0
        self._enemy_speed: float = 15.0

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
