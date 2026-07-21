import sys
import random
from arcade import Sprite, SpriteList, Vec2, Rect, LBWH

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class SSprites:
    def __init__(self, atlas: VAtlas, base_name: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList(use_spatial_hash=True)
        self.base_name: str = base_name
        self.atlas = atlas

        self.__clear_edges()

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def add_sprite(
        self,
        texture_name: str,
        center: Vec2,
        force_first_texture: bool = False,
        sprite_size: int = VData.SPRITE_SIZE,
    ) -> None:
        tile = self.atlas.pick_tile(texture_name, not force_first_texture)
        angle = random.choice(tile.allowed_angles)

        self.__up_edges(center)
        self.sprites.append(
            self.atlas.tile_to_sprite(
                tile=tile,
                center=center,
                angle=angle,
                sprite_size=sprite_size,
            )
        )

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.sprites.draw(pixelated=True)

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)

    # ########################################################################
    # ############################################################# CLEAR ####
    def clear(self) -> None:
        self.sprites.clear()
        self.__clear_edges()

    # ########################################################################
    # ############################################################# EDGES ####
    def __clear_edges(self) -> None:
        """
        !! BE CARREFUL !!
        Edges are the CENTER OF TILES which are on max of top/bot/left/right.
        They should not be used outside the class.
        """
        self.__top = -sys.maxsize
        self.__bot = sys.maxsize
        self.__left = sys.maxsize
        self.__right = -sys.maxsize

    def __up_edges(self, center: Vec2) -> None:
        """
        Save the edges.
        Used while building sprites to avoid calculations.
        """

        if center.y < self.__bot:
            self.__bot = int(center.y)
        if center.y > self.__top:
            self.__top = int(center.y)

        if center.x < self.__left:
            self.__left = int(center.x)
        if center.x > self.__right:
            self.__right = int(center.x)

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def width(self) -> int:
        """Width from edge to edge"""
        return (self.__right - self.__left) + VData.SPRITE_SIZE

    @property
    def height(self) -> int:
        """Height from edge to edge"""
        return (self.__top - self.__bot) + VData.SPRITE_SIZE

    @property
    def rect(self) -> Rect:
        """Rect from edges to edges"""
        half = VData.SPRITE_SIZE / 2
        return LBWH(
            self.__left - half, self.__bot - half, self.width, self.height
        )

    @property
    def center_position(self) -> Vec2:
        return self.rect.center

    # ########################################################################
    # ##################################################### FLOOR CORNERS ####

    @property
    def sprites_corners(self) -> list[Vec2]:
        """Return corners:  left/bot, left/top, right/top, right/bot."""

        in_bot = [s for s in self.sprites if s.center_y == self.__bot]
        in_top = [s for s in self.sprites if s.center_y == self.__top]

        bot_left = min(in_bot, key=lambda s: s.center_x)
        top_left = min(in_top, key=lambda s: s.center_x)
        top_right = max(in_top, key=lambda s: s.center_x)
        bot_right = max(in_bot, key=lambda s: s.center_x)

        return [
            Vec2(bot_left.center_x, bot_left.center_y),
            Vec2(top_left.center_x, top_left.center_y),
            Vec2(top_right.center_x, top_right.center_y),
            Vec2(bot_right.center_x, bot_right.center_y),
        ]

    # ########################################################################
    # ###################################################### FLOOR CENTER ####
    @property
    def sprite_center(self) -> Vec2:
        """Center of the sprite which is the closest to the center."""

        # Find y --
        perfect_y = (self.__top - self.__bot) / 2
        closer = min(self.sprites, key=lambda s: abs(perfect_y - s.center_y))
        y = closer.center_y

        # Middle row --
        middle_row = [f for f in self.sprites if f.center_y == y]
        middle_row.sort(key=lambda sp: sp.center_x)

        center = self.center_position.x - VData.SPRITE_SIZE
        for s in middle_row:
            if s.center_x >= center:
                return Vec2(s.center_x, s.center_y)

        return Vec2(VData.SPRITE_SIZE, VData.SPRITE_SIZE)
