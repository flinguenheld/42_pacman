from src.sprites.vatlas import VAtlas
from src.views.vend_base import VEndBase
from src.gui.titles.gtitle_victory import GTitleVictory


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░▀█▀░█▀▀░▀█▀░█▀█░█▀▄░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░▀▄▀░░█░░█░░░░█░░█░█░█▀▄░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░░▀░░░
class VVictory(VEndBase):
    def __init__(self, atlas: VAtlas, score: int) -> None:
        super().__init__(
            atlas=atlas,
            title=GTitleVictory(atlas),
            text=f"!! Congratulations !!\nYou win with {score} points !",
            score=score,
        )
