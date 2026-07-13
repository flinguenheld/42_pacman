from dataclasses import dataclass


@dataclass
class VGameState:
    _score: int = 0
    _lives: int = 3

    @property
    def score(self) -> int:
        return self._score

    @property
    def lives(self) -> int:
        return self._lives

    def increment_score(self, points: int) -> None:
        self._score += points

    def decrement_lives(self) -> None:
        if self._lives > 0:
            self._lives -= 1

    def is_game_over(self) -> bool:
        return self._lives <= 0
