import json
from pydantic import ValidationError
from src.config.model import ConfigModel
import sys
from json import JSONDecodeError, load as json_load, dumps as js_dump


class ConfigError(Exception): ...


# # TODO: PUT SOMEWHERE ELSE ?
# # TODO: CHANGE EXCEPTION TYPE ?
# def does_file_exist(file_name: str) -> str:
#     path = Path(file_name)
#     if not path.exists():
#         raise ConfigError(f"File '{file_name}' not found.")

#     return file_name


def read_json(file_name: str) -> dict[str, str | int]:

    try:
        with open(file_name, "r") as file:
            return json_load(file)

    except FileNotFoundError:
        raise ConfigError(f"File '{file_name}' not found.")

    except JSONDecodeError as e:
        raise ConfigError(f"JSON '{file_name}' -> line {e.lineno}: '{e.msg}'.")


def read_config() -> None:
    print(f"arguments: {sys.argv}")

    if len(sys.argv) != 2:
        raise ConfigError("Wrong argument number.")

    values = read_json(sys.argv[1])

    print(values)

    # try:
    ConfigModel.from_json(values)
    # except ValidationError as e:
    #     print(f"{e.errors()}\n")

    # print(values)
    # model = from_json()
