from __future__ import annotations
from src.visual.sprites.sprites import Sprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█▀█░█▀▄░▀█▀░█░█░░░▀█▀░█░█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█░█░█▀▄░░█░░░█░░░░░█░░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀▀▀░▀░▀░░▀░░░▀░░░░░▀░░▀░▀░▀▀▀░░
class SFortyTwo(Sprites):
    def __init__(self) -> None:
        super().__init__(file_basename="fortytwo")
