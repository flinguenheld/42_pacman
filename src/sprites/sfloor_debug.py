import arcade
from arcade import Sprite, SpriteList, Vec2
from pyglet.graphics import Batch

from src.config.config import Config
from src.data.enums import DebugMode
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█░░░█▀█░█▀█░█▀▄░░░█▀▄░█▀▀░█▀▄░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█░░░█░█░█░█░█▀▄░░░█░█░█▀▀░█▀▄░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░▀▀░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░
class SFloorDebug:
    def __init__(self, atlas: VAtlas) -> None:
        self.atlas = atlas
        self.setup()

    def setup(self) -> None:
        """
        Create a batch and a dict to easily update them (text & squares).
        """

        self.texts: dict[Vec2, arcade.Text] = {}
        self.texts_batch = Batch()

        self.squares: dict[Vec2, Sprite] = {}
        self.squares_batch = SpriteList[Sprite]()

    # ########################################################################
    # ####################################################### RELOAD MAZE ####
    def reload_maze(self, floors: set[Vec2]) -> None:
        """
        Reload the sprites and texts.
        Has to be done for each new maze.
        """

        self.setup()

        for point in floors:
            self.texts[point] = arcade.Text(
                "",
                x=point.x,
                y=point.y,
                anchor_x="center",
                anchor_y="center",
                align="center",
                batch=self.texts_batch,
                # bold=True,
                font_size=Config.SPRITE_SIZE * 0.4,
            )

            square_tile = self.atlas.pick_tile("debug_square")
            sprite = self.atlas.tile_to_sprite(square_tile, point)

            self.squares_batch.append(sprite)
            self.squares[point] = sprite

    # ########################################################################
    # ###################################################### UPDATE COSTS ####
    def update_costs(self, graph_costs: dict[Vec2, int]) -> None:
        """
        Update the texts and the squares according to the graph.
        Limit the amount of texts to preserve fps.
        """

        def colour(value: int) -> tuple[int, int, int]:
            if value > 45:
                value -= 45
                red = (100 + value * 2) % 255
                green = 150
                blue = (80 + value * 2) % 255
            else:
                red = (255 - value * 5) % 255
                green = (50 + value * 2) % 255
                blue = (0 + value * 3) % 255

            return (red, green, blue)

        # --
        if Config.debug_mode == DebugMode.ALGO:
            for point, cost in graph_costs.items():
                self.squares[point].color = colour(cost)
                if cost <= Config.floor_debug_max_numbers:
                    self.texts[point].text = f"{cost}"
                else:
                    self.texts[point].text = ""

            self.squares_batch.update()

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.squares_batch.draw(pixelated=True)
        self.texts_batch.draw()
