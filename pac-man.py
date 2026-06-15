from src.config.config import read_config, ConfigError

# def usage()->str:
#     return "pac-man"


def main() -> None:
    print("Hello from 42-pacman!")

    try:
        read_config()

    except ConfigError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
