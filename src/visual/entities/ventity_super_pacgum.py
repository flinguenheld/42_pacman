from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity import VEntity


# ░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█░█░█▀█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░▀▀█░█░█░█▀▀░█▀▀░█▀▄░░░█▀▀░█▀█░█░░░░
# ░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀▀▀░▀░░░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░░
class VEntitySuperPacGum(VEntity):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
    ) -> None:
        super().__init__(atlas, "super_pacgum", position)
