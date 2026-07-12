from dataclasses import dataclass


@dataclass
class VGameState:
    score: int = 0
    lives: int = 3
