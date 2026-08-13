import os
import sys
from json import JSONDecodeError

from termcolor import cprint

from src.views.vmain import VMain

# Required by PyInstaller. Changes the current working directory
# to the temporary folder where the executable is unpacked.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)


def main_bundle() -> None:
    config_path = "config.json"

    try:
        window = VMain(config_path)
        window.run()
    except (FileNotFoundError, JSONDecodeError) as e:
        cprint(f"Error: {e}\n", "light_red")
        sys.exit(1)


if __name__ == "__main__":
    main_bundle()
