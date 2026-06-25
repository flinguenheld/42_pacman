from arcade import SpriteCircle, Vec2
import arcade


class PacGum(SpriteCircle):
    def __init__(self, start_pos: Vec2) -> None:
        radius = 5
        center = start_pos
        super().__init__(
            radius=radius,
            color=arcade.color.WHITE,
            center_x=center.x,
            center_y=center.y,
        )
