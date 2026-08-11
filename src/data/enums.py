from __future__ import annotations

from enum import Enum, auto


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀█░█▄█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class VNames(Enum):
    VIEW_CHEATS = auto()
    VIEW_GAME_NEW_LEVEL = auto()
    VIEW_NEW_GAME = auto()
    VIEW_GAME_RESUME = auto()
    VIEW_GAMEOVER = auto()
    VIEW_INSTRUCTIONS = auto()
    VIEW_NEXT_LEVEL = auto()
    VIEW_PAUSE = auto()
    VIEW_PREVIOUS = auto()
    VIEW_VICTORY = auto()
    VIEW_WELCOME = auto()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░▀█▀░█░█░█░░░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░▀▀█░░█░░░█░░█░░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░░
class VStyles(Enum):
    EDGE = "edge"
    EDGE_NO_TILE = "edge_no_tile"
    EDGE_RED = "edge_red"


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░█▀▄░█░█░█▀▀░░░█▄█░█▀█░█▀▄░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀▄░█░█░█░█░░░█░█░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀▀░░
class DebugMode(Enum):
    OFF = 0
    HITBOXES = 1
    ALGO = 2
