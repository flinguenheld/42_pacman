import re
import sys

from typing import Any
from pathlib import Path
from io import TextIOWrapper
from json import JSONDecodeError
from json import loads as json_loads

from src.config.config import Config

# Needed to read config file from
# the main module/standalone executable's folder
ROOT_DIR = Path(sys.argv[0]).parent.resolve()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀░░
class ConfigError(Exception):
    pass


# ############################################################################
# ######################################################### APPLY CONFIG #####
def apply_config(file_name: str) -> None:

    values = read_json(file_name)
    Config.from_json(values)


# ############################################################################
# ############################################################ READ JSON #####
def read_json(file_name: str) -> dict[str, str | int | float] | Any:
    """
    Read the JSON file to return values in a dictionary
    Could raise:
       - FileNotFoundError
       - JSONDecodeError
    """
    file_path = ROOT_DIR / file_name

    def no_comment(file: TextIOWrapper) -> str:
        """Only get lines which start with " { }"""

        reg = re.compile("""^ *"[^"]|^ *{|^ *}""")
        return "".join(line for line in file if reg.match(line))

    try:
        with open(file_path, "r") as file:
            return json_loads(no_comment(file))

    except FileNotFoundError:
        raise ConfigError(f"File '{file_path}' not found.")

    except JSONDecodeError as e:
        raise ConfigError(f"JSON '{file_path}' -> line {e.lineno}: '{e.msg}'.")
