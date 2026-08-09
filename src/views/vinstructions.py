from arcade import Sprite, SpriteList, TextureAnimationSprite, Vec2

from src.gui.gmenu import GMenu
from src.data.vdata import VData, VNames
from src.gui.glabel import GLabel
from src.gui.gframe import GFrame
from src.gui.gwindow import GWindow
from src.gui.gbutton import GButton
from src.sprites.vatlas import VAtlas
from src.gui.titles.gtitle_instructions import GTitleInstructions


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
                separators=[16, 29],
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

        self.header_font_size_factor = 2.0
        self.font_size_factor = 1.3

        self.setup_gameplay_section()
        self.setup_entity_sprites()
        self.setup_controls_section()

        self.to_draw_and_update.extend(
            [
                self._sprite_list,
                self.menu,
            ]
        )

    def setup_gameplay_section(self) -> None:
        x_offset = -250

        start_y: int | float = 450
        self.gameplay_header = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="GAMEPLAY",
            font_size_factor=self.header_font_size_factor,
            offset_from_center_frame=Vec2(0, 450),
        )
        start_y -= 45 * self.header_font_size_factor
        self.player_instructions = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="= Player",
            font_size_factor=self.font_size_factor,
            offset_from_center_frame=Vec2(
                x_offset + VData.SPRITE_SIZE, start_y
            ),
        )
        start_y -= 60 * self.font_size_factor
        self.enemy_instructions = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="= Enemy",
            font_size_factor=self.font_size_factor,
            offset_from_center_frame=Vec2(
                x_offset + VData.SPRITE_SIZE, start_y
            ),
        )

        x_offset = 250
        start_y = 450
        start_y -= 45 * self.header_font_size_factor

        self.pacgum_instructions = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="= Pacgum",
            font_size_factor=self.font_size_factor,
            offset_from_center_frame=Vec2(
                x_offset + VData.SPRITE_SIZE, start_y
            ),
        )
        start_y -= 45 * self.font_size_factor
        self.pacgum_instructions2 = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="Collect them all to win",
            font_size_factor=self.font_size_factor,
            offset_from_center_frame=Vec2(x_offset, start_y),
        )
        start_y -= 60 * self.font_size_factor
        self.super_pacgum_instructions = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="= Super Pacgum",
            font_size_factor=self.font_size_factor,
            offset_from_center_frame=Vec2(
                x_offset + VData.SPRITE_SIZE, start_y
            ),
        )
        start_y -= 55 * self.font_size_factor
        self.super_pacgum_instructions2 = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="Invulnerability\nMakes enemies eatable for a short time",
            font_size_factor=self.font_size_factor / 1.2,
            offset_from_center_frame=Vec2(x_offset, start_y),
            multiline=True,
        )
        self.to_draw_and_update.extend(
            [
                self.gameplay_header,
                self.player_instructions,
                self.enemy_instructions,
                self.pacgum_instructions,
                self.pacgum_instructions2,
                self.super_pacgum_instructions,
                self.super_pacgum_instructions2,
            ]
        )

    def setup_entity_sprites(self) -> None:
        # Player sprite --
        self.player_sprite = self.atlas.tile_to_sprite(
            tile=self.atlas.pick_tile("player_right"),
            center=Vec2(
                self.player_instructions.left - (VData.SPRITE_SIZE * 2.0),
                self.player_instructions.center.y,
            ),
            sprite_size=int(VData.SPRITE_SIZE * self.font_size_factor * 1.2),
        )

        # Enemy sprites --
        self.enemy_0_sprite = self.atlas.tile_to_sprite(
            tile=self.atlas.pick_tile("enemy_0_chasing_right"),
            center=Vec2(
                self.enemy_instructions.left - (VData.SPRITE_SIZE * 2.0),
                self.enemy_instructions.center.y,
            ),
            sprite_size=int(VData.SPRITE_SIZE * self.font_size_factor * 1.2),
        )
        self.enemy_1_sprite = self.atlas.tile_to_sprite(
            tile=self.atlas.pick_tile("enemy_1_chasing_right"),
            center=Vec2(
                self.enemy_instructions.left - (VData.SPRITE_SIZE * 4.0),
                self.enemy_instructions.center.y,
            ),
            sprite_size=int(VData.SPRITE_SIZE * self.font_size_factor * 1.2),
        )
        self.pacgum_sprite = self.atlas.tile_to_sprite(
            tile=self.atlas.pick_tile("pacgum_wait"),
            center=Vec2(
                self.pacgum_instructions.left - (VData.SPRITE_SIZE * 2.0),
                self.pacgum_instructions.center.y,
            ),
            sprite_size=int(VData.SPRITE_SIZE * self.font_size_factor * 1.2),
        )
        self.super_pacgum_sprite = self.atlas.tile_to_sprite(
            tile=self.atlas.pick_tile("super_pacgum_wait"),
            center=Vec2(
                self.super_pacgum_instructions.left
                - (VData.SPRITE_SIZE * 2.0),
                self.super_pacgum_instructions.center.y,
            ),
            sprite_size=int(VData.SPRITE_SIZE * self.font_size_factor * 1.2),
        )
        # --
        self._sprite_list.extend(
            [
                self.player_sprite,
                self.enemy_0_sprite,
                self.enemy_1_sprite,
                self.pacgum_sprite,
                self.super_pacgum_sprite,
            ]
        )

    def setup_controls_section(self) -> None:
        controls_text = "\n".join(
            (
                "WASD/ZQSD/Arrow keys = Move player",
                "ESC = Open pause menu",
                "Space = Freeze the game",
                "T = Switch theme (before your first move)",
            )
        )

        start_y: int | float = -45
        self.controls_header = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text="CONTROLS",
            font_size_factor=self.header_font_size_factor,
            offset_from_center_frame=Vec2(0, start_y),
        )
        start_y -= 85 * self.header_font_size_factor
        self.controls_instructions = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            text=controls_text,
            multiline=True,
            font_size_factor=self.font_size_factor,
            offset_from_center_frame=Vec2(0, start_y),
        )
        self.to_draw_and_update.extend(
            [self.controls_header, self.controls_instructions]
        )

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
