from src.sprites.vatlas import VAtlas
from src.views.vend_base import VEndBase
from src.gui.titles.gtitle_game_over import GTitleGameOver


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░█▄█░█▀▀░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░█░█░█▀▀░░░█░█░▀▄▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░▀░▀░░
class VGameOver(VEndBase):
    def __init__(self, atlas: VAtlas, score: int) -> None:
        super().__init__(
            atlas=atlas,
            title=GTitleGameOver(atlas),
            text=f"Game Over\nFinal score: {score}",
            score=score,
        )
