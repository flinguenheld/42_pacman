import arcade
from arcade import Vec2, SpriteList

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀█░█▀▀░█░█░█▀▀░█▀▄░█▀█░█░█░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▄░█▀█░█░░░█▀▄░█░█░█▀▄░█░█░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░░
class GBackground:
    """
    Manage an area of sprites to display a frame.
    Used to create a window.
    """

    def __init__(
        self,
        atlas: VAtlas,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:

        self.atlas = atlas
        self.sprites: SpriteList = arcade.SpriteList()

        self.resize(x, y, width, height)
        self.build()

    # ########################################################################
    # ############################################################# BUILD ####
    def build(self) -> None:
        def add_sprite(x: int, what: str) -> int:
            tile = self.atlas.pick_tile(what)
            sprite = self.atlas.tile_to_sprite(tile, Vec2(x, y))
            self.sprites.append(sprite)
            return x + VData.SPRITE_SIZE

        def fill_line(x: int, what: str) -> int:
            while x < self.x + self.width:
                add_sprite(x, what)
                x += VData.SPRITE_SIZE
            return x

        # --
        base_wall = "wall_with_floor_on_"
        extra = "wall_extra_corner_"

        # Bottom --
        y = self.y
        x = self.x
        x = add_sprite(x, f"{extra}top_right")
        x = fill_line(x, f"{base_wall}top")
        add_sprite(x, f"{extra}top_left")

        # All middle lines --
        while y < self.y + self.height - VData.SPRITE_SIZE * 2:
            y += VData.SPRITE_SIZE
            x = self.x
            x = add_sprite(x, f"{base_wall}right")
            x = fill_line(x, "floor_hud")
            add_sprite(x, f"{base_wall}left")

        # Top --
        y += VData.SPRITE_SIZE
        x = self.x
        x = add_sprite(x, f"{extra}bot_right")
        x = fill_line(x, f"{base_wall}bottom")
        add_sprite(x, f"{extra}bot_left")

    # ########################################################################
    # ############################################################ RESIZE ####
    def resize(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.sprites.draw(pixelated=True)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self) -> Vec2:
        return Vec2(self.x + self.width / 2, self.y + self.height / 2)
