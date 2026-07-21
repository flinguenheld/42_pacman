import time
from dataclasses import dataclass


@dataclass
class VGameState:
    _score: int = 0
    _lives: int = 3

    _player_speed: float = 30.0
    _enemy_speed: float = 12.0

    time_start: float = time.time()

    @property
    def score(self) -> int:
        return self._score

    def increment_score(self, points: int) -> None:
        self._score += points

    @property
    def lives(self) -> int:
        return self._lives

    def decrement_lives(self) -> None:
        if self._lives > 0:
            self._lives -= 1

    def is_game_over(self) -> bool:
        return self._lives <= 0

    @property
    def player_speed(self) -> float:
        return self._player_speed

    @property
    def enemy_speed(self) -> float:
        return self._enemy_speed
