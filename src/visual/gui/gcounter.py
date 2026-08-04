import arcade
from arcade import Vec2
from arcade.types import Color

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.glabel import GLabel
from src.visual.gui.gframe import GFrame
from src.visual.gui.gbutton import GButton


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▀░█▀█░█░█░█▀█░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░░░█░█░█░█░█░█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
class GCounter(GButton):
    """
    A counter is a button which displays a number on its right.
    The value can be changed with arrows.
    """

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        callback: GButton.Callback,
        color: Color,
        count: int = 0,
        offset_from_center_frame: Vec2 = Vec2(0, 0),
        font_size_factor: float = 1.7,
        text: str = "",
        min: int = 0,
    ) -> None:

        # Text --
        super().__init__(
            atlas=atlas,
            frame=frame,
            callback=callback,
            offset_from_center_frame=offset_from_center_frame,
            font_size_factor=font_size_factor,
            text=text,
            color=color,
        )

        # Counter value --
        counter_offset = Vec2(
            offset_from_center_frame.x
            + self.content_width / 2
            + VData.SPRITE_SIZE,
            offset_from_center_frame.y,
        )
        self.counter_text = GLabel(
            atlas=atlas,
            frame=frame,
            offset_from_center_frame=counter_offset,
            font_size_factor=font_size_factor,
            color=color,
        )

        # --
        self.min = min
        self.count = count
        self.elements.append(self.counter_text)

    # ########################################################################
    # #################################################### COUNT PROPERTY ####
    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        if value >= self.min:
            self._count = value
            self.counter_text.text = str(value)

    # ########################################################################
    # ######################################################### KEY PRESS ####
    def on_key_press(self, symbol: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.count += 1
            case arcade.key.LEFT:
                self.count -= 1
