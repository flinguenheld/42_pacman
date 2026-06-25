from arcade import SpriteCircle, Vec2
import arcade

from src.utils.maze_grid_to_world_coords import maze_grid_to_world_coords


class PacGum(SpriteCircle):
    def __init__(self, start_grid_pos: Vec2) -> None:
        radius = 5
        center = (maze_grid_to_world_coords(start_grid_pos)) - (radius * 4)
        super().__init__(
            radius=radius,
            color=arcade.color.WHITE,
            center_x=center.x,
            center_y=center.y,
        )
