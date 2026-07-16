from collections.abc import Callable

from arcade import AStarBarrierList, Sprite, SpriteList, Vec2
import arcade
from arcade.types import Point2

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.vgamestate import VGameState
from src.visual.sprites.sfloor import SFloor
from src.visual.entities.ventity_player import VEntityPlayer
from src.visual.entities.ventity_moving import VEntityMoving


PATHFINDING_GRID_SIZE = VData.SPRITE_SIZE


class BlockedGridCells:
    def __init__(self, sprites: SpriteList[Sprite], grid_size: int):
        self.sprites = sprites
        self.grid_size = grid_size
        self.blocked_cells = self.get_blocked_cells()

    def get_blocked_cells(self) -> set[tuple[int, int]]:
        blocked_cells = set()
        for sprite in self.sprites:
            cell_x = int(sprite.center_x // self.grid_size)
            cell_y = int(sprite.center_y // self.grid_size)
            blocked_cells.add((cell_x, cell_y))
        return blocked_cells


def convert_cell_to_world_position(cell: Point2, grid_size: int) -> Vec2:
    return Vec2(cell[0] * grid_size, cell[1] * grid_size)


def convert_cells_to_world_positions(
    cells: list[Point2], grid_size: int
) -> list[Vec2]:
    return [convert_cell_to_world_position(cell, grid_size) for cell in cells]


class DFSPathfinding:
    def __init__(
        self,
        blocked_cells: BlockedGridCells,
        start_pos: Point2,
        end_pos: Point2,
        grid_size: int,
        neighbor_filter_func: Callable[
            [list[tuple[int, int]]], list[tuple[int, int]]
        ] = lambda neighbors: neighbors,
    ):
        self.blocked_cells = blocked_cells.blocked_cells
        self.start_pos = Vec2(*start_pos)
        self.end_pos = Vec2(*end_pos)
        self.grid_size = grid_size
        self.neighbor_filter_function = neighbor_filter_func

    def calculate_path(self) -> list[Vec2] | None:
        start_cell = (
            int(self.start_pos.x // self.grid_size),
            int(self.start_pos.y // self.grid_size),
        )
        end_cell = (
            int(self.end_pos.x // self.grid_size),
            int(self.end_pos.y // self.grid_size),
        )

        visited = set()
        path: list[Point2] = []

        def traverse_cells(current_cell: tuple[int, int]) -> bool:
            if current_cell == end_cell:
                path.append(current_cell)
                return True

            visited.add(current_cell)

            neighbors: list[tuple[int, int]] = [
                (current_cell[0] + 1, current_cell[1]),
                (current_cell[0] - 1, current_cell[1]),
                (current_cell[0], current_cell[1] + 1),
                (current_cell[0], current_cell[1] - 1),
            ]

            neighbors = self.neighbor_filter_function(neighbors)
            for neighbor in neighbors:
                if (
                    neighbor not in visited
                    and neighbor not in self.blocked_cells
                ):
                    if traverse_cells(neighbor):
                        path.append(current_cell)
                        return True

            return False

        if traverse_cells(start_cell):
            path.reverse()
            return convert_cells_to_world_positions(path, self.grid_size)
        else:
            return None


def player_distance_filter(
    player: VEntityPlayer,
) -> Callable[[list[tuple[int, int]]], list[tuple[int, int]]]:

    def filter_neighbors(
        neighbors: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        player_vec_2 = Vec2(
            int(player.center_x // PATHFINDING_GRID_SIZE),
            int(player.center_y // PATHFINDING_GRID_SIZE),
        )

        neighbors.sort(
            key=lambda cell: Vec2(cell[0], cell[1]).distance(player_vec_2)
        )

        return neighbors

    return filter_neighbors


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

        self.path: list[Vec2] | None = None
        self.next_position: Vec2 | None = None
        self.next_sprite: Sprite | None = None
        self.final_position: Vec2 | None = None
        self.final_sprite: Sprite | None = None
        self.closest_floor: Sprite | None = None
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.update_closest_floor()
        self.setup_barrier_list()
        self.update_next_position()

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.enemy_speed

    def setup_barrier_list(self) -> None:
        self.barrier_list = AStarBarrierList(
            self,
            self.walls.sprites,
            PATHFINDING_GRID_SIZE,
            self.maze_gen.left,
            self.maze_gen.right,
            self.maze_gen.bot,
            self.maze_gen.top,
        )

    def compute_path(self) -> None:
        closest_player_floor = self.player.get_closest_sprite(
            self.floors.sprites
        )
        if not closest_player_floor:
            self.path = None
            return
        closest_floor = self.closest_floor
        if not closest_floor:
            self.path = None
            return
        # path = arcade.astar_calculate_path(
        #     closest_floor.position,
        #     closest_player_floor.position,
        #     self.barrier_list,
        #     diagonal_movement=False,
        # )
        path = DFSPathfinding(
            BlockedGridCells(self.walls.sprites, PATHFINDING_GRID_SIZE),
            closest_floor.position,
            closest_player_floor.position,
            PATHFINDING_GRID_SIZE,
            neighbor_filter_func=player_distance_filter(self.player),
        ).calculate_path()
        if not path:
            self.path = None
            self.final_position = None
            self.final_sprite = None
            return
        self.path = path
        self.final_position = Vec2(*path[-1])
        sprites_at_final_pos = arcade.get_sprites_at_point(
            self.final_position, self.floors.sprites
        )
        if sprites_at_final_pos:
            self.final_sprite = sprites_at_final_pos[0]

    def should_recompute_path(self) -> bool:
        if not self.path or len(self.path) < 2 or not self.final_sprite:
            return True
        final_sprite_distance_to_player = arcade.get_distance_between_sprites(
            self.final_sprite, self.player
        )
        if final_sprite_distance_to_player > (2.0 * VData.SPRITE_SIZE):
            return True
        return False

    def update_next_position(self) -> None:
        if self.should_recompute_path():
            self.compute_path()
        if not self.path:
            self.next_position = None
            self.next_sprite = None
            return
        closest_floor = self.closest_floor
        if not closest_floor or not self.path:
            self.next_position = None
            self.next_sprite = None
            return
        if (
            not self.next_position
            or closest_floor.position == self.next_position
        ):
            self.path.pop(0)

            if len(self.path) > 0:
                self.next_position = Vec2(*self.path[0])
                sprites_at_next_pos = arcade.get_sprites_at_point(
                    self.next_position, self.floors.sprites
                )
                if sprites_at_next_pos:
                    self.next_sprite = sprites_at_next_pos[0]

    def update_closest_floor(self) -> Sprite | None:
        self.closest_floor = self.get_closest_sprite(self.floors.sprites)
        return self.closest_floor

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        if not self.update_closest_floor():
            return
        self.update_next_position()

        self.update_velocity(delta_time)

        self.apply_velocity()
        self.update_texture()

    def update_velocity(self, delta_time: float) -> None:
        if not self.next_position:
            self.change_x = 0
            self.change_y = 0
            return

        speed = self.apply_delta_time(self.get_speed(), delta_time)

        next_position_delta = self.next_position - self.position
        next_position_normalized = next_position_delta.normalize()

        self.change_x = next_position_normalized.x * speed * delta_time
        self.change_y = next_position_normalized.y * speed * delta_time

    def apply_velocity(self) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
