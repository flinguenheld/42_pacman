from arcade import Vec2

from src.visual import VData


def maze_grid_to_world_coords(grid_pos: Vec2) -> Vec2:
    """
    Convert maze grid coordinates to world coordinates.

    Args:
        grid_pos (Vec2): The position in the maze grid.

    Returns:
        Vec2: The corresponding world coordinates.
    """
    sprite_size: float = VData.SPRITE_SIZE
    sprite_shift: float = VData.SPRITE_SHIFT
    return Vec2(
        grid_pos.x * sprite_size + sprite_shift,
        grid_pos.y * sprite_size + sprite_shift,
    )
