from dataclasses import dataclass, field
import heapq

from arcade import Sprite, SpriteList
from arcade.types import Point2

from src.visual.pathfinding import PATHFINDING_GRID_SIZE


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
                if (
                    neighbor in self.closed_set
                    or neighbor in self.blocked_cells
                ):
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
