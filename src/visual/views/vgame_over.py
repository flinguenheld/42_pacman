from src.visual.vatlas import VAtlas
from src.visual.views.vend_base import VEndBase
from src.visual.gui.titles.gtitle_game_over import GTitleGameOver


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░░█░█░▀▄▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░▀░▀░░
class VGameOver(VEndBase):
    def __init__(self, atlas: VAtlas, score: int) -> None:
        super().__init__(
            atlas=atlas,
            title=GTitleGameOver(atlas),
            text=f"Oh no !\nYou lost with {score} points.",
            score=score,
        )
