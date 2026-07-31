from __future__ import annotations

from enum import Enum, auto
from typing import Self

from src.config.config import Config


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░░█▀█░█▀█░█▄█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░░█░█░█▀█░█░█░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class VNames(Enum):
    VIEW_GAME_RESUME = auto()
    VIEW_GAME_NEW = auto()
    VIEW_GAMEOVER = auto()
    VIEW_INSTRUCTIONS = auto()
    VIEW_PAUSE = auto()
    VIEW_PREVIOUS = auto()
    VIEW_VICTORY = auto()
    VIEW_WELCOME = auto()


class DebugMode(Enum):
    OFF = auto()
    HITBOXES = auto()
    ALGO = auto()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░░█▀▄░█▀█░▀█▀░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░░█░█░█▀█░░█░░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░░▀▀░░▀░▀░░▀░░▀░▀░░
class VData:
    """
    Useful program data, accessible everywhere in the codebase
    Used for either constants, or simply data that is rarely changed,
    or that is not tied to level changes or restarts

    Because of its special usage, it is practical
    and justified to use as a global variable

    Data tied to a level/the current game would be in the VGameState class
    (e.g the current player score)
    """

    height: int = 1300
    width: int = 1300

    debug_mode: DebugMode = DebugMode.OFF

    SPRITE_SIZE = 32
    SPRITE_SIZE_BACKGROUND = SPRITE_SIZE * 4
    TEXTURES = "textures"
    CAMERA_MARGIN: int = 100
    CAMERA_MAX_ZOOM: float = 2.8

    points_per_ghost: int = 10
    points_per_pacgum: int = 50
    points_per_super_pacgum: int = 200

    time_max: float = 90.0
    TIMER_ENEMY_DEATH: float = 10.0
    TIMER_ENEMY_FLEEING: float = 10.0

    @classmethod
    def apply_config(cls: type[Self], config: Config) -> None:
        cls.points_per_ghost = config.points_per_ghost
        cls.points_per_pacgum = config.points_per_pacgum
        cls.points_per_super_pacgum = config.points_per_super_pacgum

        cls.time_max = config.level_max_time

    # ########################################################################
    # ####################################################### _DEBUG MODE ####
    @classmethod
    def toggle_debug_mode(cls):
        match cls.debug_mode:
            case DebugMode.OFF:
                cls.debug_mode = DebugMode.HITBOXES
            case DebugMode.HITBOXES:
                cls.debug_mode = DebugMode.ALGO
            case DebugMode.ALGO:
                cls.debug_mode = DebugMode.OFF

    @classmethod
    def deactivate_debug_mode(cls):
        cls.debug_mode = DebugMode.OFF


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░▀█▀░█░█░█░░░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░▀▀█░░█░░░█░░█░░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░░
class VStyles(Enum):
    SUMMER = "summer"
    EDGE = "edge"
