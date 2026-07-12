from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity import VEntity
from src.visual.vdata import VData


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀█░█▀█░█▀▀░█▀▀░█░█░█▄█░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█▀█░█░░░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class VEntityPacGum(VEntity):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        sprite_name: str = "pacgum",
    ) -> None:
        super().__init__(atlas, sprite_name, position)

    @staticmethod
    def get_points() -> int:
        return VData.points_per_pacgum
