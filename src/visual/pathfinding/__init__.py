from collections.abc import Callable

from arcade import Sprite, SpriteList
from arcade.types import Point2

from src.visual.vdata import VData

PATHFINDING_GRID_SIZE = VData.SPRITE_SIZE

type PathfindingAlgorithm = Callable[
    [Point2, Point2, "PathfindingBarrierSet"], list[Point2]
]


class PathfindingBarrierSet:
    def __init__(self, blocked_sprites: SpriteList[Sprite]) -> None:
        self.barrier_cells: set[Point2] = set()
        for sprite in blocked_sprites:
            cell = convert_world_position_to_cell(sprite.position)
            self.barrier_cells.add(cell)


def convert_cell_to_world_position(cell: Point2) -> Point2:
    return (
        cell[0] * PATHFINDING_GRID_SIZE,
        cell[1] * PATHFINDING_GRID_SIZE,
    )


def convert_world_position_to_cell(position: Point2) -> Point2:
    return (
        int(position[0] // PATHFINDING_GRID_SIZE),
        int(position[1] // PATHFINDING_GRID_SIZE),
    )


def convert_cells_to_world_positions(cells: list[Point2]) -> list[Point2]:
    return [convert_cell_to_world_position(cell) for cell in cells]
