from dataclasses import dataclass


@dataclass
class GameState:
    score: int = 0
    lives: int = 3
