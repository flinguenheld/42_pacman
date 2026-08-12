import sys
import json
from pathlib import Path
from termcolor import cprint

from src.config.config import Config


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░░░█▀▀░█▀▀░█▀█░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░░█░░█░█░█▀█░░░▀▀█░█░░░█░█░█▀▄░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░
class HighScores:
    MAX_ENTRIES = 10
    WARNING_COLOR = "yellow"

    def __init__(self) -> None:
        # Force high scores in this folder to avoid file name checks
        self.file_name = f"highscores/{Config.highscore_filename}"
        file_path = Path(self.file_name)
        file_path.parent.mkdir(exist_ok=True)

    # ########################################################################
    # ############################################################## SAVE ####
    def save(self, player_name: str, score: int) -> None:
        """
        Open the file, get the checked values.
        Add the new one, sort and only keep the MAX ENTRIES first values.
        Replace the file with a brand new one.
        """
        if score > 0:
            # Add new score --
            entries = self._read_file()
            entries.append({"name": player_name, "score": score})

            self.sort(entries)
            while len(entries) > HighScores.MAX_ENTRIES:
                entries.pop(len(entries) - 1)

            # Overwrite file --
            try:
                with open(self.file_name, "w+") as file:
                    file.write(json.dumps(entries))
            except OSError:
                cprint(
                    "Cannot save high scores.",
                    HighScores.WARNING_COLOR,
                    file=sys.stdout,
                )

    # ########################################################################
    # ############################################################## SORT ####
    def sort(self, scores: list[dict[str, str | int]]) -> None:
        scores.sort(key=lambda e: e["name"])
        scores.sort(key=lambda e: e["score"], reverse=True)

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        entries = self._read_file()
        self.sort(entries)

        if not entries:
            return "No high score yet."

        text = ""
        for i, entry in enumerate(entries):
            text += f"{i + 1} - {entry['name']}: {entry['score']}\n"

        return text

    # ########################################################################
    # ###################################################### CHECK FORMAT ####
    def _check_format(self, values: list) -> list[dict[str, str | int]]:
        """
        Loop in the given list and exclude all entries
        which do not respect the format:
            - dict
            - entry 'name' -> str
            - entry 'score' -> int > 0
        """

        def print_msg(msg: str) -> None:
            cprint(
                f"High score file warning -> {msg}",
                HighScores.WARNING_COLOR,
                file=sys.stdout,
            )

        checked = []
        for entry in values:
            if not isinstance(entry, dict):
                print_msg("The entry is not a dictionary.")

            elif "name" not in entry or "score" not in entry:
                print_msg("Missing field 'name' or 'score'")

            elif not isinstance(entry["name"], str):
                print_msg("Invalid 'name' format (str)")

            elif not isinstance(entry["score"], int) or entry["score"] <= 0:
                print_msg("Invalid 'score' format (int >= 0)")

            else:
                checked.append(entry)

        return checked

    # ########################################################################
    # ######################################################### READ FILE ####
    def _read_file(self) -> list[dict[str, str | int]]:
        """
        Open the file, process all checks and return
        the values with a secured format.
        """

        try:
            with open(self.file_name) as file:
                return self._check_format(json.load(file))

        except OSError:
            cprint(
                "No high scores files. A new file will be created.",
                HighScores.WARNING_COLOR,
                file=sys.stdout,
            )
        except json.JSONDecodeError:
            cprint(
                "High scores files corrupted. The file will be replaced.",
                HighScores.WARNING_COLOR,
                file=sys.stdout,
            )

        return []
