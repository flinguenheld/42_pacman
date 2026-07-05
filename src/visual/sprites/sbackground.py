from arcade import Vec2
from src.visual import VData
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.ssprites import SSprites


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀█░█▀▀░█░█░█▀▀░█▀▄░█▀█░█░█░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▄░█▀█░█░░░█▀▄░█░█░█▀▄░█░█░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░░
class SBackground(SSprites):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(atlas, "background")

    def reload(self, backgrounds: set[Vec2], maze: Maze) -> None:
        """
        Clear and reload all sprites.
        Perform a check to set the simple background under the maze.
        """
        self.clear()

        maze_real_top = maze.top + VData.SPRITE_SIZE // 2
        maze_real_right = maze.right + VData.SPRITE_SIZE // 2
        maze_real_bot = maze.bot - VData.SPRITE_SIZE // 2
        maze_real_left = maze.left - VData.SPRITE_SIZE // 2

        def get_tile_edges(center: Vec2) -> dict[str, int]:
            return {
                "top": int(center.y) + VData.SPRITE_SIZE_BACKGROUND // 2,
                "right": int(center.x) + VData.SPRITE_SIZE_BACKGROUND // 2,
                "bot": int(center.y) - VData.SPRITE_SIZE_BACKGROUND // 2,
                "left": int(center.x) - VData.SPRITE_SIZE_BACKGROUND // 2,
            }

        def is_x_inside(x: int) -> bool:
            return x > maze_real_left and x < maze_real_right

        def is_y_inside(y: int) -> bool:
            return y > maze_real_bot and y < maze_real_top

        # --
        for point in backgrounds:
            force = False
            edges = get_tile_edges(point)

            if is_y_inside(edges["top"]) or is_y_inside(edges["bot"]):
                if is_x_inside(edges["left"]):
                    force = True
                if is_x_inside(edges["right"]):
                    force = True

            self.add_sprite(
                f"{self.base_name}",
                center=point,
                force_first_texture=force,
                sprite_size=VData.SPRITE_SIZE_BACKGROUND,
            )
