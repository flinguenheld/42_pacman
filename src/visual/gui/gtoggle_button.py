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

    When the button is pressed, it stays pressed until it is pressed again.
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
    # ###################################################### RUN CALLBACK ####
    def run_callback(self) -> None:
        self.pressed = not self.pressed
        self.refresh_icons()

        return super().run_callback()

    # ########################################################################
    # ##################################################### REFRESH ICONS ####
    def refresh_icons(self) -> None:
        if self.pressed:
            tile = self.atlas.pick_tile("checkbox_on")
        else:
            tile = self.atlas.pick_tile("checkbox_off")

        # --
        self.sprite_list.clear()
        self.icon_left = self.atlas.tile_to_sprite(
            tile, Vec2(self.left - VData.SPRITE_SIZE * 1.2, self.center.y - 2)
        )
        self.icon_right = self.atlas.tile_to_sprite(
            tile, Vec2(self.right + VData.SPRITE_SIZE, self.center.y - 2)
        )
        self.sprite_list.extend([self.icon_left, self.icon_right])

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        super().draw()
        self.sprite_list.draw(pixelated=True)
