from arcade import Vec2
from arcade.types import Color

from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel


class GBasicButton(GLabel):
    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        is_active: bool = False,
        position: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1,
        text: str = "",
        color: Color | None = None,
        align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
    ) -> None:
        super().__init__(
            atlas=atlas,
            frame=frame,
            position=position,
            font_size_factor=font_size_factor,
            text=text,
            color=color,
            align=align,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )
