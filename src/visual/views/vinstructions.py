from arcade import Sprite, SpriteList, TextureAnimationSprite, Vec2

from src.visual.vdata import VData, VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.glabel import GLabel
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwindow import GWindow
from src.visual.gui.gbutton import GButton
from src.visual.gui.titles.gtitle_instructions import GTitleInstructions


# ░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀█░█▀▀░▀█▀░█▀▄░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░█░█░▀▀█░░█░░█▀▄░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class VIinstructions(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitleInstructions(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=35,
                nb_cols=43,
                bevels=True,
            ),
        )

        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.menu = GMenu(
            atlas=self.atlas,
            frame=self.frame,
            widgets=[
                (
                    GButton,
                    {
                        "text": "OK",
                        "callback": lambda: self.window.switch_view(
                            VNames.VIEW_PREVIOUS
                        ),
                    },
                ),
            ],
            y_first_entry_from_frame_center=-450,
        )
        self._sprite_list: SpriteList[Sprite | TextureAnimationSprite] = (
            SpriteList()
        )

        font_size_factor = 1.4

        self.gameplay_header = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="GAMEPLAY",
            font_size_factor=2.0,
            offset_from_center_frame=Vec2(0, 425),
        )
        player_tile = self.atlas.pick_tile("player_right")
        self.player_instructions = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="= Player.",
            font_size_factor=font_size_factor,
            offset_from_center_frame=Vec2(VData.SPRITE_SIZE * 1.5, 350),
        )
        player_sprite = self.atlas.tile_to_sprite(
            tile=player_tile,
            center=Vec2(
                self.player_instructions.left - (VData.SPRITE_SIZE * 1.5),
                self.player_instructions.center.y,
            ),
            sprite_size=int(VData.SPRITE_SIZE * font_size_factor * 1.2),
        )
        self._sprite_list.append(player_sprite)
        # --
        self.controls_header = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="CONTROLS",
            font_size_factor=2.0,
            offset_from_center_frame=Vec2(0, 25),
        )
        self.controls = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text=self.controls_text,
            multiline=True,
            font_size_factor=font_size_factor,
            offset_from_center_frame=Vec2(0, -200),
        )

        self.to_draw_and_update.extend(
            [
                self._sprite_list,
                self.menu,
                self.player_instructions,
                self.gameplay_header,
                self.controls_header,
                self.controls,
            ]
        )

    # ########################################################################
    # ###################################################### INSTRUCTIONS ####
    @property
    def controls_text(self) -> str:
        controls = (
            "WASD/ZQSD/Arrow keys = Move player",
            "ESC = Open pause menu",
            "Space = Freeze the game",
            "T = Switch theme (before your first move)",
        )
        return "\n".join(controls)

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
