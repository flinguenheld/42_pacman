from __future__ import annotations

from termcolor import cprint
from dataclasses import dataclass
from typing import Generator, Tuple


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░
@dataclass
class Config:
    """Store the config data.

    Has to be fed with 'from_json()'.
    The purpose is to not block the program.
      - Seek each attribute in the json
      - Set the attribute or keep the default in case of error
      - Only print warnings if errors
    """

    _title: bool = False

    highscore_filename: str = "scores.txt"
    lives: int = 5
    pacgum: int = 42

    points_per_ghost: int = 10
    points_per_pacgum: int = 50
    points_per_super_pacgum: int = 200

    seed: int = 42
    level_max_time: int = 90

    # ########################################################################
    # ######################################################## FROM JSON #####
    def from_json(self, values_from_json: dict[str, str | int]) -> None:

        for att_name, att_value in self._next_attribute():
            # Is in the json ?
            if att_name not in values_from_json:
                self.log_default(att_name, "No value in the config file")
                continue

            # Is the same type ?
            if type(values_from_json[att_name]) is not type(att_value):
                self.log_default(att_name, "Wrong value type")
                continue

            # Per type --
            json_value = values_from_json[att_name]

            # str: is empty ?
            if type(json_value) is str:
                if len(json_value) == 0:
                    self.log_default(att_name, "Empty string")
                    continue

            # int: is supp to 0 ?
            if type(json_value) is int:
                if json_value <= 0:
                    self.log_default(att_name, "Value <= 0")
                    continue

            # Ok --
            self.__setattr__(att_name, json_value)

        self.log_close()

    # ########################################################################
    # ################################################### NEXT ATTRIBUTE #####
    def _next_attribute(self) -> Generator[Tuple[str, str | int]]:
        for key, val in vars(self).items():
            if not key.startswith("_"):
                yield key, val

    # ########################################################################
    # ############################################################## LOG #####
    def log_title(self) -> None:
        if not self._title:
            cprint(f"{'=' * 36} Config warnings {'=' * 36}", "yellow")
            self._title = True

    def log_close(self) -> None:
        if self._title:
            cprint(f"{'=' * 89}", "yellow")

    def log_default(self, field: str, message: str) -> None:
        self.log_title()
        default = getattr(self, field)
        space = " " * (30 - len(field))

        cprint(f"   Field '{field}' incorrect {space} ── {message}", "yellow")
        cprint(f"{' ' * 12} ╰─── Use default: {default}", "green")

    # ########################################################################
    # ############################################################## STR #####
    def __str__(self) -> str:
        return "\n".join(
            (
                f"{' ' * 10}- {key} -> {val}"
                for key, val in self._next_attribute()
            )
        )
