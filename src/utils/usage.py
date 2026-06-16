import sys
from typing import TextIO
from termcolor import cprint
from src.config.config import Config


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
