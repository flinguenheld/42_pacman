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

    CENTER_X: int = WIDTH // 2
    CENTER_Y: int = HEIGHT // 2

    FONT_SIZE: int = 15
    FONT_SIZE_TITLE: int = FONT_SIZE * 3

    TEXTURES = "textures"
    # TODO: I PUT 32 BUT IT COULD BE IN THE CONFIGURATION FILE
    SPRITE_SIZE = 32
    SQUARE_SIZE = SPRITE_SIZE * 3
    # TODO: FIND A WAY TO CENTER THE MAZE
    SPRITE_SHIFT = 50


class Style(Enum):
    PIRATE = "pirate"
    PIRATE_GREEN = "pirate_green"
