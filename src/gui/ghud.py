import arcade
from math import ceil
from arcade.types import Color
from arcade import Sprite, TextureAnimationSprite, Vec2, SpriteList

from src.maze.maze import Maze
from src.gui.glabel import GLabel
from src.gui.gframe import GFrame
from src.data.enums import DebugMode
from src.config.config import Config
from src.sprites.vatlas import VAtlas
from src.data.gamestate import GameState
from src.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀░░░
class VHud:
    """
    Display the score, time, level and lives in a frame.
    Reduce the font size when the maze is small.
    """

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
            nb_cols=ceil(self.maze.width / Config.SPRITE_SIZE),
            nb_rows=3,
        )
        self.icons: SpriteList[Sprite | TextureAnimationSprite] = (
            arcade.SpriteList()
        )
        self.fields_debug: dict[str, GLabel] = {}
        self.fields: dict[str, GLabel] = {}

        self.build_fields()
        self.background = GBackground(atlas)
        self.background.build(self.center_position, self.frame.rect)

    # ########################################################################
    # ############################################################# SETUP ####
    def build_fields(self) -> None:
        score_x = self.frame.width / -2 + Config.SPRITE_SIZE * 2.7
        level_x = self.frame.width / 4 - Config.SPRITE_SIZE
        lives_x = self.frame.width / 2 - Config.SPRITE_SIZE * 2.7

        self.add_field(
            entry_name="score",
            icon_name="score_hud",
            x=score_x,
            anchor_x="left",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="level",
            x=level_x,
            color=self.atlas.get_color("menu_font_active"),
            text=f"{self.gamestate.level}/{Config.amount_of_levels}",
        )

        self.add_field(
            entry_name="lives",
            icon_name="heart_hud",
            x=lives_x,
            anchor_x="right",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="timer",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="fps",
            x=self.frame.width / -4 + Config.SPRITE_SIZE,
            color=self.atlas.get_color("hud_font_debug"),
            debug=True,
        )

    # ########################################################################
    # ######################################################### ADD FIELD ####
    def add_field(
        self,
        color: Color,
        entry_name: str,
        text: str = "",
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
            text=text,
            align=anchor_x,
            anchor_x=anchor_x,
            offset_from_center_frame=Vec2(x, 2),
            color=color,
        )

        # Icon --
        if icon_name:
            match anchor_x:
                case "left":
                    x = container[entry_name].left - Config.SPRITE_SIZE / 1.3
                case "center":
                    x = container[entry_name].left - Config.SPRITE_SIZE
                case _:
                    x = container[entry_name].right + Config.SPRITE_SIZE / 1.3

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

        for text in self.fields.values():
            text.draw()

        # Debug --
        if Config.debug_mode != DebugMode.OFF:
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
    def update(self, delta_time: float) -> None:
        self.frame.update(delta_time)
        self.background.update(delta_time)
        self.icons.update_animation(delta_time)

        # --
        self.fields["lives"].text = f"{self.gamestate.lives:>2}"
        self.fields["timer"].text = self.get_time_left()
        self.fields["score"].text = str(self.gamestate.score)

        # --
        self.adapt_font_size()

    # ########################################################################
    # ################################################### ADAPT TEXT SIZE ####
    def adapt_font_size(self) -> None:
        """Reduce the font size as long as fields overlap each others."""

        while (
            self.fields["score"].rect.overlaps(self.fields["timer"].rect)
            or self.fields["level"].rect.overlaps(self.fields["timer"].rect)
            or self.fields["level"].rect.overlaps(self.fields["lives"].rect)
        ):
            for text in self.fields.values():
                text.font_size = text.font_size * 0.9
            for text in self.fields_debug.values():
                text.font_size = text.font_size * 0.9

    # ########################################################################
    # ############################################################ CENTER ####
    @property
    def center_position(self) -> Vec2:
        return self.frame.center_position
