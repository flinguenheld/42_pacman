import arcade
from arcade.types import Color
from arcade import Vec2, key, SpriteList

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█▀█░█▀█░█░█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░
class GInput:
    """Simple input which limits keys to the bare minimum"""

    MAX_LENGTH: int = 10
    FONT_SIZE_FACTOR: float = 2.5

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        color: Color,
        offset: Vec2 = Vec2(0, 0),
    ):

        font_size = atlas.font_size * GInput.FONT_SIZE_FACTOR

        # LABEL ########################
        self.label = GLabel(
            text="",
            atlas=atlas,
            frame=frame,
            offset=offset,
            font_size_factor=GInput.FONT_SIZE_FACTOR,
            color=color,
        )

        # Help ########################
        self.help_on = False
        self.help = GLabel(
            atlas=atlas,
            frame=frame,
            text="Max 10 characters, alphanumeric and spaces only",
            offset=offset + Vec2(0, font_size * 1.4),
            font_size_factor=0.8,
            color=arcade.csscolor.RED,
        )

        # Icon ########################
        tile = atlas.pick_tile("player_right")
        self.icon = atlas.tile_to_sprite(
            tile,
            Vec2(
                self.label.rect.center_x,
                self.label.rect.center_y - atlas.font_size / 2,
            ),
        )
        self.icons: SpriteList = SpriteList()
        self.icons.append(self.icon)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.label.draw()
        self.icons.draw()
        if self.help_on:
            self.help.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.icons.update_animation(delta_time)

    def up_icon_position(self) -> None:
        if self.text:
            self.icon.center_x = self.label.right + VData.SPRITE_SIZE
        else:
            self.icon.center_x = self.label.right

    # ########################################################################
    # ####################################################### KEY PRESSED ####
    def key_press_management(self, symbol: int, modifiers: int) -> None:

        if symbol == key.BACKSPACE and self.label.text:
            self.label.text = self.label.text[:-1]

        elif len(self.label.text) < GInput.MAX_LENGTH:
            if symbol >= key.A and symbol <= key.Z:
                if modifiers & 0x1 == 0x1:
                    self.label.text += chr(symbol - 32)
                else:
                    self.label.text += chr(symbol)

            if symbol >= key.KEY_0 and symbol <= key.KEY_9:
                self.label.text += chr(symbol)

            if symbol >= key.NUM_0 and symbol <= key.NUM_9:
                self.label.text += chr(symbol - 65408)

            if symbol == key.SPACE:
                self.label.text += chr(symbol)

        # --
        self.up_icon_position()

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def text(self) -> str:
        return self.label.text

    # ########################################################################
    # ####################################################### TOGGLE HELP ####
    def toggle_help(self) -> None:
        self.help_on = not self.help_on
