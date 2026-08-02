from arcade import Rect, Text, Vec2
import arcade

from src.visual.gui.gbutton import GButton
from src.visual.gui.gframe import GFrame
from src.visual.vatlas import VAtlas
from src.visual.vdata import VData


class GCounter(GButton):
    """
    A counter is a button that can be in one of two states:
    pressed or not pressed.
    When the button is pressed, it stays pressed until it is pressed again.
    """

    CHECKBOX_PADDING = VData.SPRITE_SIZE * 5

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        update_callback: "GButton.Callback[GCounter]",
        count: int = 0,
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
        self._count = 0

        self.counter_text = Text(
            text="",
            x=0,
            y=0,
            font_name=atlas.font_name,
            font_size=atlas.font_size * font_size_factor,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=atlas.get_color("menu_font"),
        )

        super().__init__(
            atlas=atlas,
            frame=frame,
            callback=update_callback,
            offset=offset,
            font_size_factor=font_size_factor,
            text=text,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            multiline=multiline,
            width=width,
            selectable=selectable,
        )

        self.count = count

        self.elements.append(self.counter_text)

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        if value < 0:
            value = 0
        self._count = value
        self.counter_text.text = str(value)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.count += 1
                self.run_callback()
            case arcade.key.LEFT:
                self.count -= 1
                self.run_callback()
            case _:
                pass

    def update_offset(self, offset: Vec2) -> None:
        offset = Vec2(
            offset.x
            - (self.counter_text.rect.width / 2)
            - (self.CHECKBOX_PADDING / 2),
            offset.y,
        )
        super().update_offset(offset)
        self.counter_text.position = Vec2(
            self.text.rect.right + self.CHECKBOX_PADDING,
            self.text.rect.center.y,
        )

    @property
    def rect(self) -> Rect:
        return self.text.rect.union(self.counter_text.rect)
