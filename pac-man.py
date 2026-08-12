import sys

from termcolor import cprint

from src.views.vmain import VMain
from src.utils.utils import print_usage
from src.config.utils import ConfigError


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise ConfigError("Wrong argument.")

        arg = sys.argv[1]
        if arg in {"-h", "--help"}:
            print_usage()
            sys.exit()

        window = VMain(config_path=arg)
        window.run()
    # QUESTION: Should we catch all exceptions here? I feel like we should
    except Exception as e:
        cprint(f"Error: {e}\n", "light_red")
        print_usage(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
