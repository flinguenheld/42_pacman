
from src.visual.gui.gframe import GFrame
from src.visual.gui.glabel import GLabel
from src.visual.vatlas import VAtlas


class GPadding(GLabel):
    def __init__(
        self, atlas: VAtlas, frame: GFrame, padding: float = 10.0
    ) -> None:
        super().__init__(atlas, frame, selectable=False)
        self.font_size_factor = padding
