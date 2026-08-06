import random
from typing import Any, Type
from arcade import Vec2, SpriteList, Sprite

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwidget import GWidget
from src.visual.gui.gbutton import GButton
from src.visual.entities.ventity_enemy import VEntityEnemy


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░░█▀▀░█▀█░▀█▀░█▀▄░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░░█▀▀░█░█░░█░░█▀▄░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░░▀░░▀░▀░░▀░░░
class GMenuEntry(GWidget):
    """
    Manage an entry for GMenu.
    Toggle its active property to draw an icon and with a special color.
    """

    FONT_SIZE_FACTOR: float = 1.7
    PADDING_ICON = VData.SPRITE_SIZE * 3

    def __init__(
        self,
        atlas: VAtlas,
        frame: GFrame,
        button_class: Type[GButton],
        kwargs: dict[str, Any],
        offset_from_frame_center: Vec2,
    ) -> None:
        super().__init__(atlas, frame)
        self.is_hoover = False

        # Since all entries are Buttons, they will need these arguments
        # No need to add them in the Views
        kwargs["atlas"] = atlas
        kwargs["frame"] = frame
        kwargs["offset_from_center_frame"] = offset_from_frame_center
        kwargs["color"] = self.atlas.get_color("menu_font")
        self.button = button_class(**kwargs)

        # --
        self.setup_icons()

    # ########################################################################
    # ####################################################### SETUP ICONS ####
    def setup_icons(self) -> None:
        # Select the icon --
        possible_tiles = ["player"]
        for id in range(self.atlas.nb_of_enemies):
            possible_tiles.append(
                f"enemy_{id}_{VEntityEnemy.Mode.CHASING.value}"
            )

        tile_name = random.choice(possible_tiles)
        self.icons: SpriteList[Sprite] = SpriteList()

        # On the left --
        tile = self.atlas.pick_tile(f"{tile_name}_right")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(
                    self.button.left - GMenuEntry.PADDING_ICON * 1.1,
                    self.button.center.y - 2,
                ),
            )
        )

        # On the right --
        tile = self.atlas.pick_tile(f"{tile_name}_left")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(
                    self.button.right + GMenuEntry.PADDING_ICON,
                    self.button.center.y - 2,
                ),
            )
        )

    # ########################################################################
    # ##################################################### TOGGLE ACTIVE ####
    def toggle_hoover(self) -> None:
        self.is_hoover = not self.is_hoover
        if self.is_hoover:
            self.button.color = self.atlas.get_color("menu_font_active")
        else:
            self.button.color = self.atlas.get_color("menu_font")

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.button.draw()

        if self.is_hoover:
            self.icons.draw(pixelated=True)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.icons.update_animation(delta_time)

    # ########################################################################
    # ################################################ HANDLE KEY PRESSES ####
    def on_key_press(self, symbol: int) -> None:
        self.button.on_key_press(symbol)
