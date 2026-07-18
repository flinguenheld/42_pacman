from typing import Protocol

from arcade import Sprite, SpriteList
from arcade.types import Point2

from src.visual.vdata import VData

PATHFINDING_GRID_SIZE = VData.SPRITE_SIZE


class PathfindingAlgorithm(Protocol):
    def __init__(
        self, start: Point2, goal: Point2, blocked_sprites: SpriteList[Sprite]
    ) -> None: ...
    def calculate_path(self) -> list[Point2]: ...
