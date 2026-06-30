from src.maze.maze_wrapper import Maze
from arcade import Vec2

from src.visual import VData


def maze_grid_to_world_coords(grid_pos: Vec2, scale: float = 2.0) -> Vec2:
    """
    Convert maze grid coordinates to world coordinates.

    Args:
        grid_pos (Vec2): The position in the maze grid.

    Returns:
        Vec2: The corresponding world coordinates.
    """

    shift_x: float = (VData.WIDTH - (Maze.WIDTH * VData.SPRITE_SIZE * 2)) / 2
    shift_y: float = (VData.HEIGHT - (Maze.HEIGHT * VData.SPRITE_SIZE * 2)) / 2

    return Vec2(
        grid_pos.x * VData.SPRITE_SIZE + shift_x,
        grid_pos.y * VData.SPRITE_SIZE + shift_y,
    )
