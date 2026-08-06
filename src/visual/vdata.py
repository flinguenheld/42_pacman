from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from src.config.config import Config


@dataclass
class VLevelData:
    maze_width: int
    maze_height: int
    # TODO: Subject isn't clear about that, it talks about a config key, then it says levels can have their own time limit
    # time_max_secs: float
    enemy_speed_multiplier: float
    player_speed_multiplier: float
    # --
    # To be set after initialization, 1-indexed (starts at 1)
    level_id: int = 0


def _set_level_ids(levels_data: list[VLevelData]) -> list[VLevelData]:
    for i, level in enumerate(levels_data):
        level.level_id = i + 1
    return levels_data


LEVELS_DATA: list[VLevelData] = _set_level_ids(
    [
        VLevelData(
            maze_width=15,
            maze_height=15,
            enemy_speed_multiplier=1.0,
            player_speed_multiplier=1.0,
        ),
        VLevelData(
            maze_width=20,
            maze_height=20,
            enemy_speed_multiplier=1.2,
            player_speed_multiplier=1.0,
        ),
    ]
)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░░█▀█░█▀█░█▄█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░░█░█░█▀█░█░█░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class VNames(Enum):
    VIEW_CHEATS = auto()
    VIEW_GAME_RESUME = auto()
    VIEW_GAME_NEW = auto()
    VIEW_GAME_NEXT_LEVEL = auto()
    VIEW_GAMEOVER = auto()
    VIEW_INSTRUCTIONS = auto()
    VIEW_PAUSE = auto()
    VIEW_PREVIOUS = auto()
    VIEW_VICTORY = auto()
    VIEW_WELCOME = auto()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░▀█▀░█░█░█░░░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░▀▀█░░█░░░█░░█░░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░░
class VStyles(Enum):
    SUMMER = "summer"
    EDGE = "edge"


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░█▀▄░█░█░█▀▀░░░█▄█░█▀█░█▀▄░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀▄░█░█░█░█░░░█░█░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀▀░░
class DebugMode(Enum):
    OFF = 0
    HITBOXES = 1
    ALGO = 2


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
    FLOOR_DEBUG_MAX_NUMBERS: int = 10

    points_per_ghost: int = 10
    points_per_pacgum: int = 50
    points_per_super_pacgum: int = 200

    time_max: float = 90.0
    TIMER_ENEMY_DEATH: float = 10.0
    TIMER_ENEMY_FLEEING: float = 10.0

    LEVELS_DATA: list[VLevelData] = LEVELS_DATA

    @classmethod
    def apply_config(cls, config: Config) -> None:
        cls.points_per_ghost = config.points_per_ghost
        cls.points_per_pacgum = config.points_per_pacgum
        cls.points_per_super_pacgum = config.points_per_super_pacgum

        cls.time_max = config.level_max_time

    # ########################################################################
    # ####################################################### _DEBUG MODE ####
    @classmethod
    def toggle_debug_mode(cls) -> None:
        cls.debug_mode = DebugMode((cls.debug_mode.value + 1) % len(DebugMode))

    @classmethod
    def deactivate_debug_mode(cls) -> None:
        cls.debug_mode = DebugMode.OFF

    @classmethod
    def is_debug_on(cls) -> bool:
        return cls.debug_mode.value > DebugMode.OFF.value
