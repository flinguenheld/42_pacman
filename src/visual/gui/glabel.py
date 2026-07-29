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
            font_size_factor: float = 1,
            text: str = "",
            color: Color | None = None,
            align: str = "center",
            anchor_x: str = "center",
            anchor_y: str = "center",
            multiline: bool = False,
            width: int | None = None,
    ) -> None:

        if not color:
            color = atlas.get_color("menu_font")
        if not text:
            text = ""

        width_for_multi = None
        if multiline and not width:
            width_for_multi = int(frame.width * 0.9)
        position = frame.center_position + offset
        self.text = Text(
            text=text,
            x=position.x,
            y=position.y,
            font_name=atlas.font_name,
            font_size=atlas.font_size * font_size_factor,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=color,
            multiline=multiline,
            width=width_for_multi,
        )

    def draw(self) -> None:
        self.text.draw()

    @property
    def left(self) -> float:
        return self.text.left

    @property
    def right(self) -> float:
        return self.text.right

    @property
    def position(self) -> Vec2:
        return Vec2(*self.text.position)

    @position.setter
    def position(self, value: Vec2) -> None:
        self.text.position = value

    @property
    def center(self) -> float:
        return self.position.x
