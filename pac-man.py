import sys
from termcolor import cprint

from src.data.vdata import VData
from src.views.vmain import VMain
from src.utils.utils import print_usage
from src.config.utils import get_config, ConfigError


def main() -> None:

    try:
        if len(sys.argv) != 2:
            raise ConfigError("Wrong argument.")

        arg = sys.argv[1]

        if arg in {"-h", "--help"}:
            print_usage()
            exit()

        else:
            print("Hello from 42-pacman!")
            config = get_config(arg)
            VData.apply_config(config)

            window = VMain()
            window.run()

    except ConfigError as e:
        cprint(f"Error: {e}\n", "light_red")
        print_usage(file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
