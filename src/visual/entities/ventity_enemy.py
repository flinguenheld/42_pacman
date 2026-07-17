from dataclasses import dataclass, field
import heapq
from typing import Protocol

from arcade import Sprite, SpriteList, Vec2
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


class PathfindingAlgorithm(Protocol):
    def __init__(
        self, start: Point2, goal: Point2, blocked_sprites: SpriteList[Sprite]
    ) -> None: ...
    def calculate_path(self) -> list[Point2]: ...


@dataclass(order=True)
class AStarOpenNode:
    f_score: float
    position: Point2 = field(compare=False)


class AStarSearch:
    def __init__(
        self, start: Point2, goal: Point2, blocked_sprites: SpriteList[Sprite]
    ) -> None:
        self.start_cell: Point2 = self.convert_world_position_to_cell(start)
        self.goal_cell: Point2 = self.convert_world_position_to_cell(goal)
        self.blocked_cells = self.get_blocked_cells(blocked_sprites)

        self.open_set: list[AStarOpenNode] = list()
        heapq.heappush(
            self.open_set,
            AStarOpenNode(
                self.heuristic(self.start_cell, self.goal_cell),
                self.start_cell,
            ),
        )

        self.closed_set: set[Point2] = set()

        self.came_from: dict[Point2, Point2] = dict()

        self.g_score: dict[Point2, float] = {self.start_cell: 0}

        self.finished = False
        self.failed = False

    def get_blocked_cells(
        self, blocked_sprites: SpriteList[Sprite]
    ) -> set[Point2]:
        blocked_cells: set[Point2] = set()
        for sprite in blocked_sprites:
            cell = self.convert_world_position_to_cell(sprite.position)
            blocked_cells.add(cell)
        return blocked_cells

    def calculate_path(self) -> list[Point2]:
        while True:
            if not self.open_set:
                self.finished = True
                self.failed = True
                return []

            current = heapq.heappop(self.open_set).position

            if current == self.goal_cell:
                reconstructed_path = self.reconstruct_path()
                path = self.convert_cells_to_world_positions(
                    reconstructed_path
                )
                self.finished = True
                return path

            self.closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closed_set:
                    continue

                if neighbor in self.blocked_cells:
                    continue

                tentative_g = self.g_score[current] + 1

                if tentative_g < self.g_score.get(neighbor, float("inf")):
                    self.came_from[neighbor] = current

                    self.g_score[neighbor] = tentative_g

                    f = tentative_g + self.heuristic(neighbor, self.goal_cell)

                    heapq.heappush(self.open_set, AStarOpenNode(f, neighbor))

    def heuristic(self, a: Point2, b: Point2) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, cell: Point2) -> list[Point2]:
        return [
            (cell[0] + 1, cell[1]),
            (cell[0] - 1, cell[1]),
            (cell[0], cell[1] + 1),
            (cell[0], cell[1] - 1),
        ]

    def reconstruct_path(self) -> list[Point2]:
        current = self.goal_cell

        path = [current]

        while current != self.start_cell:
            current = self.came_from[current]

            path.append(current)

        path.reverse()

        return path

    def convert_cell_to_world_position(self, cell: Point2) -> Point2:
        return (
            cell[0] * PATHFINDING_GRID_SIZE,
            cell[1] * PATHFINDING_GRID_SIZE,
        )

    def convert_world_position_to_cell(self, position: Point2) -> Point2:
        return (
            int(position[0] // PATHFINDING_GRID_SIZE),
            int(position[1] // PATHFINDING_GRID_SIZE),
        )

    def convert_cells_to_world_positions(
        self, cells: list[Point2]
    ) -> list[Point2]:
        return [self.convert_cell_to_world_position(cell) for cell in cells]


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
        pathfinder: type[PathfindingAlgorithm] = AStarSearch,
    ) -> None:
        super().__init__(atlas, f"enemy_{id}", position)
        self.floors: SFloor = floors
        self.walls: SWall = walls
        self.player: VEntityPlayer = player
        self.gamestate: VGameState = gamestate
        self.maze_gen: Maze = maze_gen
        self.pathfinder: type[PathfindingAlgorithm] = pathfinder

        self.path: list[Point2] | None = None
        self.next_position: Point2 | None = None
        self.next_sprite: Sprite | None = None
        self.target_position: Point2 | None = None
        self.target_sprite: Sprite | None = None
        self.closest_floor: Sprite | None = None
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.update_closest_floor()
        self.update_next_position()

    # ########################################################################
    # ############################################################# SPEED ####
    def get_speed(self) -> int:
        return self.gamestate.enemy_speed

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

        path = self.pathfinder(
            start=closest_floor.position,
            goal=closest_player_floor.position,
            blocked_sprites=self.walls.sprites,
        ).calculate_path()

        if not path:
            self.path = None
            self.target_position = None
            self.target_sprite = None
            return
        self.path = path
        self.target_position = closest_player_floor.position
        sprites_at_target_pos = arcade.get_sprites_at_point(
            self.target_position, self.floors.sprites
        )
        if sprites_at_target_pos:
            self.target_sprite = sprites_at_target_pos[0]

    def should_recompute_path(self) -> bool:
        if not self.path or len(self.path) < 2 or not self.target_sprite:
            return True
        distance_to_player_from_target_sprite = (
            arcade.get_distance_between_sprites(
                self.target_sprite, self.player
            )
        )
        if distance_to_player_from_target_sprite > (2.0 * VData.SPRITE_SIZE):
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
                self.next_position = self.path[0]
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

        next_position_delta = Vec2(*self.next_position) - Vec2(*self.position)
        next_position_normalized = next_position_delta.normalize()

        self.change_x = next_position_normalized.x * speed * delta_time
        self.change_y = next_position_normalized.y * speed * delta_time

    def apply_velocity(self) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
