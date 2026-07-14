from arcade import AStarBarrierList, Vec2
import arcade

from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.vatlas import VAtlas
from src.visual.sprites.sfloor import SFloor
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_moving import VEntityMoving
from src.visual.vdata import VData
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
        maze_gen: Maze,
    ) -> None:
        super().__init__(atlas, f"enemy_{id}", position)
        self.floors: SFloor = floors
        self.walls: SWall = walls
        self.player: VEntityPlayer = player
        self.gamestate: VGameState = gamestate
        self.maze_gen: Maze = maze_gen

        self.barrier_list: AStarBarrierList
        self.next_position: Vec2 | None
        self.path: list[tuple[float, float]] | None

        arcade.schedule(lambda delta_time: self.calculate_next_position(), 0.5)
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.setup_barrier_list()
        self.calculate_next_position()
        # self.change_y = -10

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.enemy_speed

    def setup_barrier_list(self) -> None:
        self.barrier_list = AStarBarrierList(
            self,
            self.walls.sprites,
            VData.SPRITE_SIZE,
            self.maze_gen.left,
            self.maze_gen.right,
            self.maze_gen.bot,
            self.maze_gen.top,
        )

    def calculate_next_position(self) -> None:
        closest_player_floor = arcade.get_closest_sprite(
            self.player, self.floors.sprites
        )
        if not closest_player_floor:
            self.next_position = None
            return
        (closest_player_floor, _) = closest_player_floor
        closest_enemy_floor = arcade.get_closest_sprite(
            self, self.floors.sprites
        )
        if not closest_enemy_floor:
            self.next_position = None
            return
        (closest_enemy_floor, _) = closest_enemy_floor
        path = arcade.astar_calculate_path(
            closest_enemy_floor.position,
            closest_player_floor.position,
            self.barrier_list,
            diagonal_movement=False,
        )
        self.path = path
        if path:
            if len(path) > 1:
                self.next_position = Vec2(*path[1])
            else:
                self.next_position = None
        else:
            self.next_position = None

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        # self.update_velocity()
        # self.calculate_next_position()

        if self.next_position:
            next_position = self.next_position
            next_position_delta = next_position - self.position
            self.position = (
                (next_position_delta.normalize() * 16)
                * self.get_speed()
                * delta_time
            ) + self.position
        else:
            self.change_x = 0
            self.change_y = 0

        self.update_texture()
