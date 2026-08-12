import os
import sys
from json import JSONDecodeError

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

from termcolor import cprint

from src.views.vmain import VMain


def main_bundle() -> None:
    config_path = "test_config.json"

    try:
        window = VMain(config_path)
        window.run()
    # QUESTION: Should we catch all exceptions here? I feel like we should
    except (FileNotFoundError, JSONDecodeError) as e:
        cprint(f"Error: {e}\n", "light_red")
        sys.exit(1)


if __name__ == "__main__":
    main_bundle()
