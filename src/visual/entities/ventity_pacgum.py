from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity import VEntity


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀█░█▀█░█▀▀░█▀▀░█░█░█▄█░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█▀█░█░░░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class VEntityPacGum(VEntity):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
    ) -> None:
        super().__init__(atlas, "pacgum", position)
