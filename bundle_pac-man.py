from termcolor import cprint

from src.views.vmain import VMain


def main_bundle() -> None:
    config_path = "test_config.json"

    try:
        window = VMain(config_path)
        window.run()
    # QUESTION: Should we catch all exceptions here? I feel like we should
    except Exception as e:
        cprint(f"Error: {e}\n", "light_red")
        exit(1)
