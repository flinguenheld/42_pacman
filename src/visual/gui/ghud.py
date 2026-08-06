import arcade
from math import ceil
from arcade.types import Color
from arcade import Sprite, TextureAnimationSprite, Vec2, SpriteList

from src.maze.maze import Maze
from src.visual.vdata import VData, DebugMode
from src.visual.vatlas import VAtlas
from src.visual.gui.glabel import GLabel
from src.visual.gui.gframe import GFrame
from src.visual.gamestate import GameState
from src.visual.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀░░░
class VHud:
    OFFSET: int = 10000

    def __init__(
        self,
        maze: Maze,
        atlas: VAtlas,
        gamestate: GameState,
    ) -> None:

        self.maze = maze
        self.atlas = atlas
        self.gamestate = gamestate

        self.frame = GFrame(
            atlas,
            bot_left=Vec2(VHud.OFFSET, VHud.OFFSET),
            nb_cols=ceil(self.maze.width / VData.SPRITE_SIZE),
            nb_rows=3,
        )
        self.icons: SpriteList[Sprite | TextureAnimationSprite] = (
            arcade.SpriteList()
        )
        self.fields_debug: dict[str, GLabel] = dict()
        self.fields: dict[str, GLabel] = dict()

        self.build_fields()
        self.background = GBackground(atlas)
        self.background.build(self.center_position, self.frame.rect)

    # ########################################################################
    # ############################################################# SETUP ####
    def build_fields(self) -> None:
        self.font_size = VData.SPRITE_SIZE * 0.6
        self.y_text_line = VHud.OFFSET + VData.SPRITE_SIZE

        self.add_field(
            entry_name="score",
            icon_name="score_hud",
            x=self.frame.width / -2 + VData.SPRITE_SIZE * 3.2,
            anchor_x="left",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="lives",
            icon_name="heart_hud",
            x=self.frame.width / 2 - VData.SPRITE_SIZE * 3.2,
            anchor_x="right",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="timer",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="fps",
            x=self.frame.width / -4,
            color=self.atlas.get_color("hud_font_debug"),
            debug=True,
        )

    # ########################################################################
    # ######################################################### ADD FIELD ####
    def add_field(
        self,
        color: Color,
        entry_name: str,
        icon_name: str | None = None,
        anchor_x: str = "center",
        x: float = 0,
        debug: bool = False,
    ) -> None:
        # Field --
        container = self.fields_debug if debug else self.fields
        container[entry_name] = GLabel(
            atlas=self.atlas,
            frame=self.frame,
            align=anchor_x,
            anchor_x=anchor_x,
            offset_from_center_frame=Vec2(x, 2),
            color=color,
        )

        # Icon --
        if icon_name:
            match anchor_x:
                case "left":
                    x = container[entry_name].left - VData.SPRITE_SIZE / 1.3
                case "center":
                    x = container[entry_name].left - VData.SPRITE_SIZE
                case _:
                    x = container[entry_name].right + VData.SPRITE_SIZE / 1.3

            tile = self.atlas.pick_tile(icon_name)
            self.icons.append(
                self.atlas.tile_to_sprite(
                    tile,
                    Vec2(x, self.frame.center_position.y),
                )
            )

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.background.draw()
        self.frame.draw()
        self.icons.draw(pixelated=True)

        self.fields["score"].text = str(self.gamestate.score)
        self.fields["lives"].text = f"{self.gamestate.lives:>2}"
        self.fields["timer"].text = self.get_time_left()

        for text in self.fields.values():
            text.draw()

        # Debug --
        if VData.debug_mode != DebugMode.OFF:
            self.fields_debug["fps"].text = f"FPS: {arcade.get_fps():.2f}"
            for text in self.fields_debug.values():
                text.draw()

    # ########################################################################
    # ##################################################### GET TIME LEFT ####
    def get_time_left(self) -> str:
        if self.gamestate.timer <= 0:
            return "OVER"

        minutes = int(self.gamestate.timer) // 60
        seconds = int(self.gamestate.timer) % 60

        return f"{minutes:02}:{seconds:02}"

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.frame.update(delta_time)
        self.background.update(delta_time)
        self.icons.update_animation(delta_time)

    # ########################################################################
    # ############################################################ CENTER ####
    @property
    def center_position(self) -> Vec2:
        return self.frame.center_position
