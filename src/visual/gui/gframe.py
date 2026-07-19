from arcade import Vec2, SpriteList, LBWH, Rect

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█▀▄░█▀█░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀▄░█▀█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀░▀░▀░▀░▀▀▀░░
class GFrame:
    """
    Manage an area of sprites to display a frame.
    Logic is reversed from maze -_-
    """

    WALL = "wall_with_floor_on_"
    EXTRA = "wall_extra_corner_"

    def __init__(
        self,
        atlas: VAtlas,
        x: int = 0,
        y: int = 0,
        width: int = 1000,
        height: int = 1000,
        separators: list[int] = [],
    ) -> None:

        self.atlas = atlas
        self.sprites: SpriteList = SpriteList()

        self.separators = separators

        self.resize(x, y, width, height)
        self.build()

    # ########################################################################
    # ############################################################# BUILD ####
    def build(self) -> None:

        self.sprites.clear()
        y = self.y

        # Bottom #######################################
        y = self._build_bot(y)

        # Middle #######################################
        while y <= self.y + self.height - VData.SPRITE_SIZE * 2:
            if self.pop_separator(y):
                print(f"triggered here: {y}")
                y = self.build_separator(y)
            else:
                y = self._build_line(
                    y,
                    f"{GFrame.WALL}right",
                    "floor_hud",
                    f"{GFrame.WALL}left",
                )

        # Top ##########################################
        y = self._build_top(y)

        print(f"y={y}")

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def _add_sprite(self, x: int, y: int, what: str) -> int:
        tile = self.atlas.pick_tile(what)
        sprite = self.atlas.tile_to_sprite(tile, Vec2(x, y))
        self.sprites.append(sprite)
        return x + VData.SPRITE_SIZE

    # ########################################################################
    # ######################################################## BUILD LINE ####
    def _build_line(self, y: int, left: str, middle: str, right: str) -> int:
        x = self.x
        x = self._add_sprite(x, y, left)
        while x < self.x + self.width:
            x = self._add_sprite(x, y, middle)
        self._add_sprite(x, y, right)
        return y + VData.SPRITE_SIZE

    # ########################################################################
    # ################################################### BUILD TOP / BOT ####
    def _build_top(self, y: int) -> int:
        self._build_line(
            y,
            f"{GFrame.EXTRA}bot_right",
            f"{GFrame.WALL}bottom",
            f"{GFrame.EXTRA}bot_left",
        )
        return y + VData.SPRITE_SIZE

    def _build_bot(self, y: int) -> int:
        self._build_line(
            y,
            f"{GFrame.EXTRA}top_right",
            f"{GFrame.WALL}top",
            f"{GFrame.EXTRA}top_left",
        )
        return y + VData.SPRITE_SIZE

    # ########################################################################
    # ################################################### BUILD SEPARATOR ####
    def build_separator(self, y: int) -> int:
        y = self._build_top(y)
        y = self._build_bot(y)
        return y

    # ########################################################################
    # ##################################################### POP SEPARATOR ####
    def pop_separator(self, current_y: int) -> bool:
        """
        Get the first value which is higher than trigger,
        remove it and return True
        """
        for sep in self.separators:
            print(f"check {current_y}, {sep}")
            if current_y + VData.SPRITE_SIZE >= self.y + sep:
                self.separators.remove(sep)
                return True

        return False

    # ########################################################################
    # ############################################################ RESIZE ####
    def resize(self, x: int, y: int, width: int, height: int) -> None:
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

    @property
    def rect(self) -> Rect:
        return LBWH(self.x, self.y, self.width, self.height)
