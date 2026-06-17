from src.visual.vmenu import VMenu
from src.visual.vmain import VMain
import sys
from termcolor import cprint
from src.utils.usage import print_usage
from src.config.utils import get_config, ConfigError


def main() -> None:

    try:
        if len(sys.argv) != 2:
            raise ConfigError("Wrong argument.")

        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_usage()
            exit()

        else:
            get_config(sys.argv[1])
            window = VMain()
            window.show_view(VMenu())
            window.run()

        print("Hello from 42-pacman!")

    except ConfigError as e:
        cprint(f"Error: {e}\n", "light_red")
        print_usage(file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
