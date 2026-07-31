from arcade import Text, Vec2
from arcade.types import Color

from src.visual.vatlas import VAtlas
from src.visual.gui.gwidget import GWidget
from src.visual.gui.gframe import GFrame


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░░░█▀█░█▀▄░█▀▀░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀█░█▀▄░█▀▀░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀▀▀░░
class GLabel(GWidget):
    """Text wrapper with common default values"""

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        offset: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.0,
        text: str = "",
        color: Color | None = None,
        align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
        multiline: bool = False,
        width: int | None = None,
        selectable: bool = False,
    ) -> None:
        super().__init__(atlas, frame)
        self.font_size_factor = font_size_factor
        self.selectable = selectable

        if not color:
            color = atlas.get_color("menu_font")
        if not text:
            text = ""

        width_for_multi = None
        if multiline and not width:
            width_for_multi = int(frame.width * 0.9)
        self.text = Text(
            text=text,
            x=0,
            y=0,
            font_name=atlas.font_name,
            font_size=atlas.font_size * font_size_factor,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=color,
            multiline=multiline,
            width=width_for_multi,
        )
        self.update_offset(offset)

        self.elements.append(self.text)

    @property
    def left(self) -> float:
        return self.text.rect.left

    @property
    def right(self) -> float:
        return self.text.rect.right

    def update_offset(self, offset: Vec2) -> None:
        self.text.position = self.frame.center_position + offset

    @property
    def center(self) -> Vec2:
        return Vec2(*self.text.rect.center)

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
        self.update_color()

    def update_color(self) -> None:
        pass
