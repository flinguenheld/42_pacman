from arcade import SpriteCircle, Vec2
import arcade
from arcade.types import Point2


class PacGum(SpriteCircle):
    def __init__(self, start_pos: Point2) -> None:
        radius = 5
        center = start_pos
        super().__init__(
            radius=radius,
            color=arcade.color.WHITE,
            center_x=center[0],
            center_y=center[1],
        )
