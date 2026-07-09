from arcade import SpriteCircle, Vec2
import arcade


class PacGum(SpriteCircle):
    def __init__(self, position: Vec2) -> None:
        radius = 5
        center = position
        super().__init__(
            radius=radius,
            color=arcade.color.WHITE,
            center_x=center[0],
            center_y=center[1],
        )
