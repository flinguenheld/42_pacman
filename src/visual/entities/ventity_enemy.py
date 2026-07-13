from arcade import Vec2

from src.visual.sprites.swall import SWall
from src.visual.vatlas import VAtlas
from src.visual.sprites.sfloor import SFloor
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.vgamestate import VGameState


# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▀░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityEnemy(VEntityMoving):
    def __init__(
        self,
        id: int,
        atlas: VAtlas,
        position: Vec2,
        floors: SFloor,
        walls: SWall,
        player: VEntityPlayer,
        gamestate: VGameState,
    ) -> None:
        super().__init__(atlas, f"enemy_{id}", position)
        self.floors: SFloor = floors
        self.walls: SWall = walls
        self.player: VEntityPlayer = player
        self.gamestate: VGameState = gamestate
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        pass
        # self.change_y = -10

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.enemy_speed

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        # self.update_velocity()
        self.update_texture()
