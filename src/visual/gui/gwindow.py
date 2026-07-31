import arcade.gui
from typing import Any
from arcade import Vec2

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.titles.gtitle import GTitle
from src.visual.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░▀█▀░█▀█░█▀▄░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░░█░░█░█░█░█░█░█░█▄█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░░
class GWindow(arcade.View):
    """
    Create and manage a window with one Title and one frame.

    Fill the 'to_draw_and_update' list with widgets
    to automatically display them.
    """

    def __init__(self, atlas: VAtlas, title: GTitle, frame: GFrame) -> None:
        super().__init__()
        self.atlas = atlas
        VData.deactivate_debug_mode()

        # Frame --
        self.frame = frame

        # Title --
        self.title = title
        self.title.build(
            Vec2(
                self.frame.center_position.x,
                self.frame.rect.top + VData.SPRITE_SIZE * 2,
            )
        )

        # Background --
        arcade.set_background_color(self.atlas.get_color("background"))
        self.background = GBackground(atlas)
        self.background.build(
            center=self.frame.center_position,
            to_avoid=[self.frame.rect, self.title.rect],
        )

        self.to_draw_and_update: list[Any] = [
            self.background,
            self.frame,
            self.title,
        ]

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
            for widget in self.to_draw_and_update:
                widget.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def on_update(self, delta_time: int | float) -> None:
        for widget in self.to_draw_and_update:
            if hasattr(widget, "update"):
                widget.update(delta_time)

    # ########################################################################
    # ############################################### ON RESIZE / ON SHOW ####
    def on_resize(self, width: int, height: int) -> None:
        self.cameras_init()

    def on_show_view(self) -> None:
        self.cameras_init()
