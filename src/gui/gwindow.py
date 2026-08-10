import arcade
from arcade import Vec2

from src.data.vdata import VData
from src.gui.gframe import GFrame
from src.gui.gwidget import GWidget
from src.sprites.vatlas import VAtlas
from src.gui.titles.gtitle import GTitle
from src.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░▀█▀░█▀█░█▀▄░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░░█░░█░█░█░█░█░█░█▄█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░░
class GWindow(arcade.View, GWidget):
    """
    Create and manage a window with one Title and one frame.

    Fill the 'to_draw_update_press_release' list with widgets
    to automatically display them.
    """

    def __init__(self, atlas: VAtlas, title: GTitle, frame: GFrame) -> None:
        GWidget.__init__(self, atlas, frame)
        arcade.View.__init__(self)
        VData.deactivate_debug_mode()

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

        self.to_draw_update_press_release.extend(
            [self.background, self.frame, self.title]
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
    # ################################################## ON RESIZE / SHOW ####
    def on_resize(self, width: int, height: int) -> None:
        self.cameras_init()

    def on_show_view(self) -> None:
        self.cameras_init()

    # ########################################################################
    # ################################################## ON DRAW / UPDTAE ####
    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            GWidget.draw(self)

    def on_update(self, delta_time: int | float) -> None:
        GWidget.update(self, delta_time)

    # ########################################################################
    # ############################################ ON KEY PRESS / RELEASE ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        GWidget.key_press(self, symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        GWidget.key_release(self, symbol, modifiers)
