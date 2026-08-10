from arcade.types import Color
from arcade import Vec2, Text, Rect

from src.gui.gframe import GFrame
from src.gui.gwidget import GWidget
from src.sprites.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░░░█▀█░█▀▄░█▀▀░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀█░█▀▄░█▀▀░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀▀▀░░
class GLabel(GWidget):
    """Widget which manages an arcade.Text with common default values."""

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        text: str = "",
        offset_from_center_frame: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1,
        color: Color | None = None,
        align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
        multiline: bool = False,
        width: int | None = None,  # Only for multilines
    ):
        super().__init__(atlas, frame)

        if not color:
            color = atlas.get_color("menu_font")
        if not text:
            text = ""

        width_for_multi = None
        if multiline and not width:
            width_for_multi = int(frame.width * 0.9)

        self._text_widget = Text(
            text=text,
            x=frame.center_position.x + offset_from_center_frame.x,
            y=frame.center_position.y + offset_from_center_frame.y,
            font_name=atlas.font_name,
            font_size=atlas.font_size * font_size_factor,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=color,
            multiline=multiline,
            width=width_for_multi,
        )

        self.to_draw_update_press_release.append(self._text_widget)

    # ########################################################################
    # ########################################################## GEOMETRY ####
    @property
    def rect(self) -> Rect:
        return self._text_widget.rect

    @property
    def left(self) -> float:
        return self.rect.left

    @property
    def right(self) -> float:
        return self.rect.right

    @property
    def center(self) -> Vec2:
        return self.rect.center

    @property
    def content_width(self) -> int:
        return self._text_widget.content_width

    # ########################################################################
    # ############################################################## TEXT ####
    @property
    def text(self) -> str:
        return self._text_widget.text

    @text.setter
    def text(self, value: str) -> None:
        self._text_widget.text = value

    # ########################################################################
    # ############################################################# COLOR ####
    @property
    def color(self) -> Color:
        return self._text_widget.color

    @color.setter
    def color(self, value: Color) -> None:
        self._text_widget.color = value
