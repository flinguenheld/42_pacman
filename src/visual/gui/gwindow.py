import arcade.gui
from arcade import Vec2

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.title.gtitle import GTitle
from src.visual.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░▀█▀░█▀█░█▀▄░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░░█░░█░█░█░█░█░█░█▄█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░░
class GWindow(arcade.View):
    """Create and manage a window with one Title and one frame"""

    def __init__(self, atlas: VAtlas, title: GTitle, frame: GFrame) -> None:
        super().__init__()
        self.atlas = atlas

        # Frame --
        self.frame = frame

        # Title --
        self.title = title
        self.title.set_postion(
            int(self.frame.center_position.x),
            int(
                self.frame.center_position.y
                + self.frame.height // 2
                + title.height * 0.7
            ),
        )

        # Background --
        self.background = GBackground(atlas)
        self.background.build(
            center=self.frame.center_position,
            to_avoid=[self.frame.rect, self.title.rect],
        )

        self.cameras_init()

    # ########################################################################
    # ########################################################### CAMERAS ####
    def cameras_init(self) -> None:
        position = self.frame.center_position
        position += Vec2(0, self.title.height / 2)

        width_to_scale = max(self.frame.width, self.title.width)
        scale_hori = self.width / (width_to_scale + VData.CAMERA_MARGIN)
        scale_vert = self.height / (self.frame.height + VData.CAMERA_MARGIN)

        zoom = min(scale_hori, scale_vert)
        if zoom > VData.CAMERA_MAX_ZOOM:
            zoom = VData.CAMERA_MAX_ZOOM

        self.camera = arcade.Camera2D(
            self.window.rect,
            position=position,
            zoom=zoom,
        )

    # ########################################################################
    # ############################################################## DRAW ####
    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.background.draw()
            self.frame.draw()
            self.title.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        self.background.update(delta_time)
        self.frame.update(delta_time)
        self.title.update(delta_time)

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        self.cameras_init()
