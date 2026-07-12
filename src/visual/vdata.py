from enum import Enum


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░░█▀█░█▀█░█▄█░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░░█░█░█▀█░█░█░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░
class VNames(Enum):
    VIEW_MENU = 0
    VIEW_GAME = 1
    VIEW_PAUSE = 2


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░░█▀▄░█▀█░▀█▀░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░░█░█░█▀█░░█░░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░░▀▀░░▀░▀░░▀░░▀░▀░░
class VData:
    """
    Useful program data, accessible everywhere in the codebase
    Used for either constants, or simply data that is rarely changed,
    or that is not tied to level changes or restarts

    Because of its special usage, it is practical and justified to use as a global variable

    Data tied to a level/the current game would be in the VGameState class
    (e.g the current player score)
    """
    height: int = 1300
    width: int = 1300

    FONT_SIZE: int = 15
    FONT_SIZE_TITLE: int = FONT_SIZE * 3

    SPRITE_SIZE = 32
    SPRITE_SIZE_BACKGROUND = SPRITE_SIZE * 4
    TEXTURES = "textures"
    CAMERA_MARGIN: int = 100


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░▀█▀░█░█░█░░░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░▀▀█░░█░░░█░░█░░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░░
class VStyles(Enum):
    SUMMER = "summer"
    EDGE = "edge"
