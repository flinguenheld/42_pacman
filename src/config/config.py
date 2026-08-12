from __future__ import annotations

from termcolor import cprint
from typing import ClassVar, Any
from dataclasses import dataclass

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

    # ################################################
    # ### Manageable variables with the config file ##
    lives: ClassVar[int] = 3

    points_per_ghost: ClassVar[int] = 10
    points_per_pacgum: ClassVar[int] = 50
    points_per_super_pacgum: ClassVar[int] = 200

    first_level_seed: ClassVar[int] = 42
    first_level_width: ClassVar[int] = 8
    first_level_height: ClassVar[int] = 8

    amount_of_levels: ClassVar[int] = 10
    amount_of_enemies: ClassVar[int] = 4

    timer_level: ClassVar[float] = 90.0
    timer_enemy_death: ClassVar[float] = 10.0
    timer_enemy_fleeing: ClassVar[float] = 10.0

    highscore_filename: ClassVar[str] = "scores.json"

    floor_debug_max_numbers: ClassVar[int] = 10

    window_height: ClassVar[int] = 1300
    window_width: ClassVar[int] = 1300

    # ################################################
    # #################### Non manageable variables ##
    debug_mode: ClassVar[DebugMode] = DebugMode.OFF

    SPRITE_SIZE: ClassVar[int] = 32
    SPRITE_SIZE_BACKGROUND: ClassVar[int] = SPRITE_SIZE * 4
    TEXTURE_FOLDER: ClassVar[str] = "textures"

    CAMERA_MARGIN: ClassVar[int] = 100
    CAMERA_MAX_ZOOM: ClassVar[float] = 2.8

    # Set which attributes are manageables and their limits --
    MANAGEABLE_FIELDS: ClassVar[dict[str, dict[str, str | int | float]]] = {
        "lives": {"min": 1, "max": 100},
        # --
        "points_per_ghost": {"min": 0},
        "points_per_pacgum": {"min": 0},
        "points_per_super_pacgum": {"min": 0},
        # --
        "first_level_seed": {"min": 1},
        "first_level_width": {"min": 5, "max": 20},
        "first_level_height": {"min": 7, "max": 20},
        # --
        "amount_of_levels": {"min": 1, "max": 1000},
        "amount_of_enemies": {"min": 0, "max": 1000},
        # --
        "timer_level": {"min": 5.0, "max": 200.0},
        "timer_enemy_death": {"min": 5.0, "max": 200.0},
        "timer_enemy_fleeing": {"min": 5.0, "max": 200.0},
        # --
        "highscore_filename": {"filename": True},
        # --
        "floor_debug_max_numbers": {"min": 5, "max": 50},
        # --
        "window_height": {"min": 100, "max": 5000},
        "window_width": {"min": 100, "max": 5000},
    }

    # ########################################################################
    # ######################################################## FROM JSON #####
    @classmethod
    def from_json(cls, values_from_json: dict[str, str | int | float]) -> None:

        for att_name, info in cls.MANAGEABLE_FIELDS.items():
            default_value = getattr(cls, att_name)

            # Is in the json ?
            if att_name not in values_from_json:
                cls.log_default(att_name, "No value in the config file")
                continue

            # --
            json_value = values_from_json[att_name]

            # Is the same type ?
            if type(json_value) is not type(default_value):
                cls.log_default(
                    att_name,
                    f"Wrong value type, must be -> {type(default_value)}",
                    wrong_val=json_value,
                )
                continue

            # str: is empty ?
            if type(json_value) is str:
                if len(json_value) == 0:
                    cls.log_default(att_name, "Empty string")
                    continue
                if info.get("filename", False) and (
                    len(json_value) < 5
                    or not all(
                        c.isalnum() or c in ["_", "-", "."] for c in json_value
                    )
                ):
                    cls.log_default(
                        att_name,
                        "Filename: (only: [a-z][0-9][_-.], min 5 chars)",
                        wrong_val=json_value,
                    )
                    continue

            # int/float: is in the min/max ?
            if type(json_value) is int or type(json_value) is float:
                if "min" in info and float(json_value) < float(info["min"]):
                    cls.log_default(
                        att_name,
                        f"Must be minimum: {info['min']}",
                        wrong_val=json_value,
                    )
                    continue
                if "max" in info and float(json_value) > float(info["max"]):
                    cls.log_default(
                        att_name,
                        f"Must be maximum: {info['max']}",
                        wrong_val=json_value,
                    )
                    continue

            # Ok --
            setattr(cls, att_name, json_value)

        cls.log_close()

    # ########################################################################
    # ############################################################## LOG #####
    @classmethod
    def log_title(cls) -> None:
        if not cls._title:
            cprint(f"{'=' * 36} Config warnings {'=' * 36}", "yellow")
            cls._title = True

    @classmethod
    def log_close(cls) -> None:
        if cls._title:
            cprint(f"{'=' * 89}", "yellow")

    @classmethod
    def log_default(
        cls,
        field: str,
        message: str,
        wrong_val: Any = "",
    ) -> None:
        cls.log_title()
        default = getattr(cls, field)
        space = " " * (30 - len(field))

        if wrong_val:
            cprint(
                f"   Field '{field}' incorrect. {space} ──> "
                f"'{wrong_val}': {message}",
                "yellow",
            )
        else:
            cprint(
                f"   Field '{field}' incorrect {space} ──>  {message}",
                "yellow",
            )

        cprint(f"{' ' * 12} ╰─── Use default: {default}", "green")

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
