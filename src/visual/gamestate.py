from __future__ import annotations
import random
from src.visual.vdata import VData


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
        self.setup()

    def setup(self) -> None:
        """
        Initializes the game state with default values.
        Let's us reset the game state in a more elegant way
        """
        # TODO: Check if this is the right solution for that problem
        self.score = 0
        self.lives = 3
        self.timer = VData.time_max

        self._player_speed: float = 30.0
        self._enemy_speed: float = 15.0
        self._enemy_patroling_trigger: float = 7

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
        return self._enemy_speed * random.uniform(0.8, 1.2)

    # ########################################################################
    # ################################################# PATROLING TRIGGER ####
    @property
    def enemy_patroling_trigger(self) -> int:
        # QUESTION: Is it good here ?
        return int(self._enemy_patroling_trigger * random.uniform(0.5, 1.5))
