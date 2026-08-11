import sys
import random
from arcade import Sprite, SpriteList, Vec2, Rect, LBWH

from src.config.config import Config
from src.sprites.vatlas import VAtlas


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
        sprite_size: int = Config.SPRITE_SIZE,
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
        return (self.__right - self.__left) + Config.SPRITE_SIZE

    @property
    def height(self) -> int:
        """Height from edge to edge"""
        return (self.__top - self.__bot) + Config.SPRITE_SIZE

    @property
    def rect(self) -> Rect:
        """Rect from edges to edges"""
        half = Config.SPRITE_SIZE / 2
        return LBWH(
            self.__left - half, self.__bot - half, self.width, self.height
        )

    @property
    def center_position(self) -> Vec2:
        return self.rect.center

    # ########################################################################
    # ############################################ SPRITE CORNER / CENTER ####
    @property
    def sprite_corners(self) -> list[Vec2]:
        """Return corners:  left/bot, left/top, right/top, right/bot."""

        return [
            self.find_closest_sprite_of(self.rect.bottom_left),
            self.find_closest_sprite_of(self.rect.top_left),
            self.find_closest_sprite_of(self.rect.top_right),
            self.find_closest_sprite_of(self.rect.bottom_right),
        ]

    @property
    def sprite_center(self) -> Vec2:
        """Center of the sprite which is the closest to the real center."""

        return self.find_closest_sprite_of(self.center_position)

    # ########################################################################
    # ############################################### FIND CLOSEST SPRITE ####
    def find_closest_sprite_of(self, point: Vec2) -> Vec2:
        """
        Loop in all sprites to find the closest one.
        Return its center position
        """

        current = self.sprites[0]
        current_distance = float(sys.maxsize)

        for sprite in self.sprites:
            d = point.distance(Vec2(sprite.center_x, sprite.center_y))
            if d < current_distance:
                current = sprite
                current_distance = d

        return Vec2(current.center_x, current.center_y)
