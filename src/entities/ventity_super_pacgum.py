from arcade import Vec2

from src.data.vdata import VData
from src.sprites.vatlas import VAtlas
from src.entities.ventity_pacgum import VEntityPacGum


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
    def get_points() -> int:
        return VData.points_per_super_pacgum
