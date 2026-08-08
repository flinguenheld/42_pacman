from __future__ import annotations
import random
from src.data.vdata import VData


class Cheats:
    def __init__(self, game_state: GameState) -> None:
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
    def __init__(self) -> None:
        self.score = 0
        self.lives = 3
        self.level = 1
        self.reset_timer()

        self._player_speed: float = 30.0
        self._enemy_speed: float = 15.0
        self._enemy_patrolling_trigger: float = 7

        self.cheats: Cheats = Cheats(self)

    def next_level(self) -> None:
        self.level += 1
        self.reset_timer()

    def reset_timer(self) -> None:
        self.timer = VData.time_max

    # ########################################################################
    # ##################################################### SCORE & LIVES ####
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
    @property
    def player_speed(self) -> float:
        return self._player_speed

    # QUESTION: I put that here in case you want to adapt the level difficulty
    #           The trigger is the distance from the player an enemy will turn
    #           into chasing mode.
    #           We can imagine tons of ways to deal with:
    #             - simply fixed in VEntityEnemy
    #             - linked to the level
    #             - linked to the maze size
    #             - ...
    @property
    def enemy_speed(self) -> float:
        # QUESTION: Is it good here ?
        level_factor = 1 + ((self.level - 1) * 0.01)
        random_factor = random.uniform(0.8, 1.1)

        speed = self._enemy_speed * level_factor * random_factor
        # Cap the speed to avoid enemies being too fast
        return min(speed, self.player_speed * 0.9)

    # ########################################################################
    # ################################################ PATROLLING TRIGGER ####
    @property
    def enemy_patrolling_trigger(self) -> int:
        return int(self._enemy_patrolling_trigger * random.uniform(0.5, 1.5))
