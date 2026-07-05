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
    HEIGHT: int = 1300
    WIDTH: int = 1300

    # TODO: REMOVE THAT UGLY
    CENTER_X: int = WIDTH // 2
    CENTER_Y: int = HEIGHT // 2

    FONT_SIZE: int = 15
    FONT_SIZE_TITLE: int = FONT_SIZE * 3

    SPRITE_SIZE = 32
    SPRITE_SIZE_BACKGROUND = SPRITE_SIZE * 4
    TEXTURES = "textures"
    CAMERA_MARGIN: int = 100


class Style(Enum):
    TINY_BATTLE = "tiny_battle"
    PIRATE = "pirate"
    PIRATE_GREEN = "pirate_green"
    SUMMER = "summer"
    EDGE = "test"
