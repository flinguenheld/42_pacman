import arcade
from arcade.types import Color
from arcade import Sprite, SpriteList, Vec2

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.gbutton import GButton


# ░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█▀█░█▀▀░█▀▀░█░░░█▀▀░░░█▀▄░█░█░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░█░█░░█░░█░█░█░█░█░█░█░░░█▀▀░░░█▀▄░█░█░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀░░▀▀▀░░▀░░░▀░░▀▀▀░▀░▀░░
class GToggleButton(GButton):
    """
    A toggle button is a button that can be in one of two states:
       - pressed
       - not pressed

    The value can be changed with arrows.
    """

    CHECKBOX_PADDING = VData.SPRITE_SIZE * 5

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: GButton.Callback,
        pressed: bool = False,
        offset_from_center_frame: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.7,
        text: str = "",
        color: Color | None = None,
    ) -> None:

        super().__init__(
            atlas=atlas,
            frame=frame,
            callback=callback,
            offset_from_center_frame=offset_from_center_frame,
            font_size_factor=font_size_factor,
            text=text,
            color=color,
        )
        self.pressed = pressed
        self.sprite_list: SpriteList[Sprite] = SpriteList()
        self.refresh_icons()

    # ########################################################################
    # ##################################################### REFRESH ICONS ####
    def refresh_icons(self) -> None:
        self.sprite_list.clear()

        if self.pressed:
            tile = self.atlas.pick_tile("checkbox_on")
        else:
            tile = self.atlas.pick_tile("checkbox_off")

        icon_position = Vec2(
            self.center.x + self.content_width / 2 + VData.SPRITE_SIZE,
            self.center.y - 4,
        )

        self.icon = self.atlas.tile_to_sprite(tile, icon_position)
        self.sprite_list.append(self.icon)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        super().draw()
        self.sprite_list.draw(pixelated=True)

    # ########################################################################
    # ######################################################### KEY PRESS ####
    def on_key_press(self, symbol: int) -> None:
        if symbol in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.pressed = not self.pressed
            self.refresh_icons()
