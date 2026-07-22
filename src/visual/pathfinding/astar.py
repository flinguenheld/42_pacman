from dataclasses import dataclass, field
import heapq

from arcade.types import Point2

from src.visual.pathfinding import (
    PathfindingBarrierSet,
    convert_cells_to_world_positions,
    convert_world_position_to_cell,
)


@dataclass(order=True)
class AStarOpenNode:
    f_score: float
    position: Point2 = field(compare=False)


def astar_search(
    start: Point2, goal: Point2, barrier_set: PathfindingBarrierSet
) -> list[Point2]:
    start_cell = convert_world_position_to_cell(start)
    goal_cell = convert_world_position_to_cell(goal)

    open_set: list[AStarOpenNode] = []
    heapq.heappush(
        open_set,
        AStarOpenNode(
            f_score=_astar_heuristic(start_cell, goal_cell),
            position=start_cell,
        ),
    )

    closed_set: set[Point2] = set()

    came_from: dict[Point2, Point2] = {}

    g_score: dict[Point2, float] = {start_cell: 0}

    while open_set:
        current = heapq.heappop(open_set).position

        if current == goal_cell:
            reconstructed_path = _astar_reconstruct_path(
                goal_cell, start_cell, came_from
            )
            return convert_cells_to_world_positions(reconstructed_path)

        closed_set.add(current)

        for neighbor in _astar_get_neighbors(current):
            if neighbor in closed_set or neighbor in barrier_set.barrier_cells:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f = tentative_g + _astar_heuristic(neighbor, goal_cell)

                heapq.heappush(open_set, AStarOpenNode(f, neighbor))
    return []


def _astar_heuristic(a: Point2, b: Point2) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _astar_get_neighbors(cell: Point2) -> list[Point2]:
    return [
        (cell[0] + 1, cell[1]),
        (cell[0] - 1, cell[1]),
        (cell[0], cell[1] + 1),
        (cell[0], cell[1] - 1),
    ]


def _astar_reconstruct_path(
    goal_cell: Point2, start_cell: Point2, came_from: dict[Point2, Point2]
) -> list[Point2]:
    current = goal_cell
    path = [current]
    while current != start_cell:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
