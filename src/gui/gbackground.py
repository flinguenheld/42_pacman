from arcade import SpriteList, Vec2, LBWH, Rect

from src.config.config import Config
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀█░█▀▀░█░█░█▀▀░█▀▄░█▀█░█░█░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▄░█▀█░█░░░█▀▄░█░█░█▀▄░█░█░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░░
class GBackground:
    """
    Manage a large spritelist with large sprites.
    Perform a check to only use the first sprite when it will be under the
    to_avoid rectangle.
    """

    def __init__(self, atlas: VAtlas):
        self.atlas = atlas
        self.sprites: SpriteList = SpriteList()

    # ########################################################################
    # ############################################################# BUILD ####
    def build(self, center: Vec2, to_avoid: Rect | list[Rect]) -> None:
        self.sprites.clear()

        top = int(center.y + Config.height)
        bot = int(center.y - Config.height)

        left = int(center.x - Config.width)
        right = int(center.x + Config.width)

        sprite_size = Config.SPRITE_SIZE_BACKGROUND
        sprite_name = "background"

        if not isinstance(to_avoid, list):
            to_avoid = [to_avoid]

        for x in range(left, right, sprite_size):
            for y in range(bot, top, sprite_size):
                random_on = self.does_not_overlap(x, y, to_avoid)

                tile = self.atlas.pick_tile(sprite_name, random_on)
                sprite = self.atlas.tile_to_sprite(
                    tile,
                    Vec2(x, y),
                    sprite_size=sprite_size,
                )

                self.sprites.append(sprite)

    # ########################################################################
    # ######################################################### OVERLAP ? ####
    def does_not_overlap(self, x: int, y: int, to_avoid: list[Rect]) -> bool:

        rect = LBWH(
            x - Config.SPRITE_SIZE_BACKGROUND // 2,
            y - Config.SPRITE_SIZE_BACKGROUND // 2,
            Config.SPRITE_SIZE_BACKGROUND,
            Config.SPRITE_SIZE_BACKGROUND,
        )

        return not any(rect.overlaps(ta) for ta in to_avoid)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.sprites.draw(pixelated=True)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)
