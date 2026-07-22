from arcade import Text, Vec2
from arcade.types import Color

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░░░█▀█░█▀▄░█▀▀░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█▀█░█▀▄░█▀▀░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀▀▀░░
class GLabel(Text):
    """Text wrapper with common default values"""

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        text: str = "",
        offset: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1,
        color: Color | None = None,
        align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
        multiline: bool = False,
        width: int | None = None,  # Only for multilines
    ):

        if not color:
            color = atlas.get_color("menu_font")
        if not text:
            text = ""

        width_for_multi = None
        if multiline and not width:
            width_for_multi = int(frame.width * 0.9)

        super().__init__(
            text=text,
            x=frame.center_position.x + offset.x,
            y=frame.center_position.y + offset.y,
            font_name=atlas.font_name,
            font_size=atlas.font_size * font_size_factor,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=color,
            multiline=multiline,
            width=width_for_multi,
        )
