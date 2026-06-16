import re
from typing import Any
from io import TextIOWrapper
from json import JSONDecodeError, loads as json_loads

from src.config.config import Config


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀░░
class ConfigError(Exception):
    pass


# ############################################################################
# ############################################################# GET JSON #####
def get_config(file_name: str) -> Config:

    values = read_json(file_name)

    config = Config()
    config.from_json(values)
    return config


# ############################################################################
# ############################################################ READ JSON #####
def read_json(file_name: str) -> dict[str, str | int] | Any:
    """
    Read the JSON file to return values in a dictionary
    Could raise:
       - FileNotFoundError
       - JSONDecodeError
    """

    def no_comment(file: TextIOWrapper) -> str:
        """Only get lines which start with " { }"""

        reg = re.compile("""^ *"[^"]|^ *{|^ *}""")
        return "".join((line for line in file.readlines() if reg.match(line)))

    try:
        with open(file_name, "r") as file:
            return json_loads(no_comment(file))

    except FileNotFoundError:
        raise ConfigError(f"File '{file_name}' not found.")

    except JSONDecodeError as e:
        raise ConfigError(f"JSON '{file_name}' -> line {e.lineno}: '{e.msg}'.")
