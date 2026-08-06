import sys
from typing import TextIO
from termcolor import cprint
from arcade import Sprite, Vec2

from src.visual.vdata import VData
from src.config.config import Config

# TODO: Rename this file to utils ?


# ############################################################################
# ########################################################## PRINT USAGE #####
def print_usage(file: TextIO = sys.stdout) -> None:

    cprint("Usage: ", "yellow", end="", file=file)
    cprint("uv run python pac-man.py ", "magenta", end="", file=file)
    cprint("[CONFIG_FILE]", file=file)
    cprint("       uv run python pac-man.py ", "magenta", end="", file=file)
    cprint("--help", file=file)
    cprint("", file=file)
    cprint("Argument: ", "yellow", file=file)
    cprint("   [CONFIG_FILE]", "light_blue", file=file)
    cprint(
        "     JSON format file configuration to override defaults.",
        file=file,
    )
    cprint(Config(), file=file)
    cprint("", file=file)
    cprint("   --help, -h", "light_green", file=file)
    cprint("     Print this message and exit.", file=file)


# ############################################################################
# ######################################################## SPRITE CENTER #####
# QUESTION: Put here but is it really clean ?
#           It's a visual util...
#           Maybe an overload of Sprite could be another solution...
#           No, it could be a pain with spritelists
def sprite_center(sprite: Sprite) -> Vec2:
    return Vec2(sprite.center_x, sprite.center_y)


# ############################################################################
# ########################################################## PRINT DEBUG #####
def print_debug(text: str, color: str = "magenta", end: str = "\n"):
    if VData.is_debug_on:
        cprint(f"   {text}", color=color, end=end)
