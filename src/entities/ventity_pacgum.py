from arcade import Vec2

from src.data.vdata import VData
from src.sprites.vatlas import VAtlas
from src.entities.ventity import VEntity


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
