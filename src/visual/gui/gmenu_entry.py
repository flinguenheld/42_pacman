from __future__ import annotations
import random

from arcade import Sprite, TextureAnimationSprite, Vec2, SpriteList
from src.visual.gamestate import GameState

from src.visual.gui.gwidget import GWidget
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▄█░█▀▀░█▀█░█░█░░░█▀▀░█▀█░▀█▀░█▀▄░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▀░█░█░█░█░░░█▀▀░█░█░░█░░█▀▄░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░░▀░░▀░▀░░▀░░░
class GMenuEntry:
    """
    Manage an entry for GMenu.
    Toggle its active property to draw an icon and with a special color.
    Save a ToCall object to launch with call_action().
    """

    def __init__(
        self,
        atlas: VAtlas,
        widget: GWidget,
        offset: Vec2,
    ) -> None:

        self.atlas = atlas
        self.widget = widget
        self._active = False

        widget.update_offset(offset)
        center = widget.center

        # Icons --
        shift = (self.widget.center.x / 2) + VData.SPRITE_SIZE

        # QUESTION: Is it clean ?
        possible_tiles = ["player"]
        for id in range(self.atlas.nb_of_enemies):
            possible_tiles.append(f"enemy_{id}_{GameState.Mode.CHASING.value}")

        tile_name = random.choice(possible_tiles)

        self.icons = SpriteList[Sprite | TextureAnimationSprite]()
        tile = self.atlas.pick_tile(f"{tile_name}_right")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(center.x - shift - 5, center.y - 5),
            )
        )

        tile = self.atlas.pick_tile(f"{tile_name}_left")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(center.x + shift, center.y - 5),
            )
        )

    # ########################################################################
    # ####################################################### CALL ACTION ####
    def run_callback(self) -> None:
        self.widget.run_callback()

    # ########################################################################
    # ##################################################### TOGGLE ACTIVE ####
    @property
    def active(self) -> bool:
        return self.widget.active

    @active.setter
    def active(self, value: bool) -> None:
        self.widget.active = value

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.widget.draw()

        if self.active:
            self.icons.draw(pixelated=True)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.icons.update_animation(delta_time)  # type: ignore
