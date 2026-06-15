from __future__ import annotations

from dataclasses import dataclass
from termcolor import cprint
from typing import Annotated, Any, ClassVar
from pydantic import BaseModel, Field, field_validator


def check_type(value_type: Any, default: Any):
    def inner(func):
        def wrapper(*args, **kwargs):

            if not isinstance(args[1], value_type):
                return ConfigModel.log_default(
                    kwargs["field"], "Wrong type", default
                )

            return func(*args, **kwargs)

        return wrapper

    return inner


def check_none(field: str, value_type: Any, default: Any):
    def inner(func):
        def wrapper(*args, **kwargs):

            if args[1] is None:
                return ConfigModel.log_default(field, "Not given", default)

            return func(*args, **kwargs)

        return wrapper

    return inner


@dataclass
class ConfigModel:
    title: ClassVar[bool] = False

    highscore_filename: Any
    lives: Any
    # pacgum: Annotated[int, Field(min=1, max=200)]

    # points_per_ghost: Annotated[int, Field(min=1, max=200)]
    # points_per_pacgum: Annotated[int, Field(min=1, max=200)]
    # points_per_super_pacgum: Annotated[int, Field(min=1, max=200)]

    # seed: Annotated[int, Field(min=1, max=100)]
    # level_max_time: Annotated[int, Field(min=1, max=100)]
    def __post_init__(self) -> None:
        self.lives = self.check_lives(self.lives, field="lives")

    @check_type(field="lives", value_type=int, default=5)
    def check_lives(self, value: Any):
        if value is None:
            return ConfigModel.log_default("lives", "Not given", 5)
        return value

    # ########################################################################
    # ###################################################### LOG DEFAULT #####
    @staticmethod
    def log_default(field: str, message: str, default: str | int) -> str | int:

        if not ConfigModel.title:
            cprint(f"{'=' * 10} Config error {'=' * 10}", "yellow")
            ConfigModel.title = True

        cprint(f"Field '{field}' incorrect -> {message}", "yellow")
        cprint(f"    -> Use the default value: {field}={default}", "green")
        return default

    # ########################################################################
    # ######################################################## FROM JSON #####
    @staticmethod
    def from_json(values: dict[str, str | int]) -> ConfigModel:
        blah = ConfigModel(
            highscore_filename=values.get("highscore_filename"),
            lives=values.get("lives"),
        )
        return blah
