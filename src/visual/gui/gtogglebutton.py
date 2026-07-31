from arcade import Sprite, SpriteCircle, SpriteList, Vec2
import arcade

from src.visual.gui.gbutton import GButton
from src.visual.gui.gframe import GFrame
from src.visual.vatlas import VAtlas
from src.visual.vdata import VData


class GToggleButton(GButton):
    """
    A toggle button is a button that can be in one of two states:
    pressed or not pressed.
    When the button is pressed, it stays pressed until it is pressed again.
    """

    CHECKBOX_PADDING = VData.SPRITE_SIZE * 10

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: "GToggleButton.Callback",
        pressed: bool = False,
        offset: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.7,
        text: str = "",
        align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
        multiline: bool = False,
        width: int | None = None,
        selectable: bool = True,
    ) -> None:
        self.pressed = pressed

        self.checkbox = SpriteCircle(
            radius=int(atlas.font_size * font_size_factor * 0.5),
            color=arcade.color.GREEN if self.pressed else arcade.color.RED,
        )
        self._checkbox_sprite_list: SpriteList[Sprite] = SpriteList()
        self._checkbox_sprite_list.append(self.checkbox)

        super().__init__(
            atlas=atlas,
            frame=frame,
            callback=callback,
            offset=offset,
            font_size_factor=font_size_factor,
            text=text,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            multiline=multiline,
            width=width,
            selectable=selectable
        )

        self.elements.append(self._checkbox_sprite_list)

    def run_callback(self) -> None:
        self.pressed = not self.pressed
        self.checkbox.color = (
            arcade.color.GREEN if self.pressed else arcade.color.RED
        )
        return super().run_callback()

    def update_offset(self, offset: Vec2) -> None:
        offset = Vec2(
            offset.x
            - (self.checkbox.rect.width / 2)
            - (self.CHECKBOX_PADDING / 2),
            offset.y,
        )
        super().update_offset(offset)
        self.checkbox.position = Vec2(
            self.text.rect.right + self.CHECKBOX_PADDING,
            self.text.rect.center.y,
        )

    @property
    def left(self) -> float:
        return self.text.rect.left

    @property
    def right(self) -> float:
        return self.checkbox.rect.right

    @property
    def center(self) -> Vec2:
        return (self.text.rect.center + self.checkbox.rect.center) / 2
