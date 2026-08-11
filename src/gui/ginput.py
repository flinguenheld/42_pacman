from arcade.types import Color
from arcade import Sprite, Vec2, key, SpriteList

from src.gui.gframe import GFrame
from src.gui.glabel import GLabel
from src.gui.gwidget import GWidget
from src.config.config import Config
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█▀█░█▀█░█░█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░░▀░░░
class GInput(GWidget):
    """Simple input which limits keys to the bare minimum."""

    MAX_LENGTH: int = 10
    FONT_SIZE_FACTOR: float = 2.5

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        color: Color,
        offset_from_frame_center: Vec2 = Vec2(0, 0),
    ):
        super().__init__(atlas, frame)

        font_size = atlas.font_size * GInput.FONT_SIZE_FACTOR

        # LABEL ########################
        self.label = GLabel(
            text="",
            atlas=atlas,
            frame=frame,
            offset_from_center_frame=offset_from_frame_center,
            font_size_factor=GInput.FONT_SIZE_FACTOR,
            color=color,
        )

        # Help ########################
        self.help_on = False
        self.help = GLabel(
            atlas=atlas,
            frame=frame,
            text="Max 10 characters, alphanumeric and spaces only",
            offset_from_center_frame=offset_from_frame_center
            + Vec2(0, font_size * 1.4),
            font_size_factor=0.7,
            color=color,
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
        self.icons = SpriteList[Sprite]()
        self.icons.append(self.icon)

        # --
        self.to_draw_update_press_release.extend(
            [self.label, self.icons, self.help]
        )

    # ########################################################################
    # ####################################################### KEY PRESSED ####
    def key_press(self, symbol: int, modifiers: int) -> None:
        super().key_press(symbol, modifiers)

        if symbol == key.BACKSPACE and self.text:
            self.text = self.text[:-1]

        elif len(self.text) < GInput.MAX_LENGTH:
            if symbol >= key.A and symbol <= key.Z:
                if modifiers & 0x1 == 0x1:
                    self.text += chr(symbol - 32)
                else:
                    self.text += chr(symbol)

            if symbol >= key.KEY_0 and symbol <= key.KEY_9:
                self.text += chr(symbol)

            if symbol >= key.NUM_0 and symbol <= key.NUM_9:
                self.text += chr(symbol - 65408)

            if symbol == key.SPACE:
                self.text += chr(symbol)

        # --
        self.update_icon_position()

    # ########################################################################
    # ############################################## UPDATE ICON POSITION ####
    def update_icon_position(self) -> None:
        if self.text:
            self.icon.center_x = self.label.right + Config.SPRITE_SIZE
        else:
            self.icon.center_x = self.label.right

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def text(self) -> str:
        return self.label.text

    @text.setter
    def text(self, value: str) -> None:
        self.label.text = value
