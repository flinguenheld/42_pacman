from __future__ import annotations

from termcolor import cprint
from dataclasses import dataclass
from typing import Generator, Tuple, ClassVar

from src.data.enums import DebugMode


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░
@dataclass
class Config:
    """Store the config data.
       Useful program data, accessible everywhere in the codebase.


    Has to be fed with 'from_json()'.
    The purpose is to not block the program.
      - Seek each attribute in the json
      - Set the attribute or keep the default in case of error
      - Only print warnings if errors
    """

    _title: bool = False

    # Manageable variables with the config file --
    lives: ClassVar[int] = 3

    points_per_ghost: ClassVar[int] = 10
    points_per_pacgum: ClassVar[int] = 50
    points_per_super_pacgum: ClassVar[int] = 200

    seed_first_level: ClassVar[int] = 42
    amount_of_levels: ClassVar[int] = 10
    amount_of_enemies: ClassVar[int] = 4

    timer_level: ClassVar[float] = 90.0
    timer_enemy_death: ClassVar[float] = 10.0
    timer_enemy_fleeing: ClassVar[float] = 10.0

    highscore_filename: ClassVar[str] = "scores.txt"
    floor_debug_max_numbers: ClassVar[int] = 10
    texture_folder: ClassVar[str] = "textures"

    height: ClassVar[int] = 1300
    width: ClassVar[int] = 1300

    # Non manageable variable --
    debug_mode: ClassVar[DebugMode] = DebugMode.OFF

    SPRITE_SIZE: ClassVar[int] = 32
    SPRITE_SIZE_BACKGROUND: ClassVar[int] = SPRITE_SIZE * 4

    CAMERA_MARGIN: ClassVar[int] = 100
    CAMERA_MAX_ZOOM: ClassVar[float] = 2.8

    # ########################################################################
    # ######################################################## FROM JSON #####
    @classmethod
    def from_json(cls, values_from_json: dict[str, str | int | float]) -> None:

        for att_name, att_value in cls._next_manageable_attribute():
            # Is in the json ?
            if att_name not in values_from_json:
                cls.log_default(att_name, "No value in the config file")
                continue

            # Is the same type ?
            if type(values_from_json[att_name]) is not type(att_value):
                cls.log_default(att_name, "Wrong value type")
                continue

            # Per type --
            json_value = values_from_json[att_name]

            # str: is empty ?
            if type(json_value) is str:
                if len(json_value) == 0:
                    cls.log_default(att_name, "Empty string")
                    continue

            # int: is supp to 0 ?
            if type(json_value) is int:
                if json_value <= 0:
                    cls.log_default(att_name, "Value <= 0")
                    continue

            # float: is supp to 0 ?
            if type(json_value) is float:
                if json_value <= 0.0:
                    cls.log_default(att_name, "Value <= 0.0")
                    continue

            # Ok --
            setattr(cls, att_name, att_value)

        cls.log_close()

    # ########################################################################
    # ######################################## NEXT MANAGEABLE ATTRIBUTE #####
    @classmethod
    def _next_manageable_attribute(
        cls,
    ) -> Generator[Tuple[str, str | int | float]]:
        manageable_fields = [
            "lives",
            "points_per_ghost",
            "points_per_pacgum",
            "points_per_super_pacgum",
            "seed_first_level",
            "amount_of_levels",
            "amount_of_enemies",
            "timer_level",
            "timer_enemy_death",
            "timer_enemy_fleeing",
            "highscore_filename",
            "floor_debug_max_numbers",
            "texture_folder",
            "height",
            "width",
        ]

        for key in manageable_fields:
            yield key, getattr(cls, key)

    # ########################################################################
    # ############################################################## LOG #####
    @classmethod
    def log_title(self) -> None:
        if not self._title:
            cprint(f"{'=' * 36} Config warnings {'=' * 36}", "yellow")
            self._title = True

    @classmethod
    def log_close(self) -> None:
        if self._title:
            cprint(f"{'=' * 89}", "yellow")

    @classmethod
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
                for key, val in self._next_manageable_attribute()
            )
        )

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
