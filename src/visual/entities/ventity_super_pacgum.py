from arcade import Vec2

from src.visual.entities.ventity_pacgum import VEntityPacGum
from src.visual.vatlas import VAtlas
from src.visual.vdata import VData


# ░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█░█░█▀█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░▀▀█░█░█░█▀▀░█▀▀░█▀▄░░░█▀▀░█▀█░█░░░░
# ░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀▀▀░▀░░░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░░
class VEntitySuperPacGum(VEntityPacGum):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
    ) -> None:
        super().__init__(atlas, position, sprite_name="super_pacgum")

    @staticmethod
    def get_score() -> int:
        return VData.points_per_super_pacgum
