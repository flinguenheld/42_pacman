import time
import arcade
from arcade.types import Color
from arcade import Text, Vec2, SpriteList

from src.maze.maze import Maze
from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.visual.gui.gframe import GFrame
from src.visual.vgamestate import VGameState
from src.visual.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀█░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀░░░
class VHud:
    OFFSET: int = 10000

    def __init__(
        self,
        maze: Maze,
        atlas: VAtlas,
        gamestate: VGameState,
    ) -> None:

        self.maze = maze
        self.atlas = atlas
        self.gamestate = gamestate

        self.frame = GFrame(
            atlas,
            bot_left=Vec2(VHud.OFFSET, VHud.OFFSET),
            nb_cols=self.maze.width // VData.SPRITE_SIZE + 1,
            nb_rows=3,
        )
        self.icons: SpriteList = arcade.SpriteList()
        self.fields_debug: dict[str, Text] = dict()
        self.fields: dict[str, Text] = dict()

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
            x=VHud.OFFSET + VData.SPRITE_SIZE * 2.5,
            anchor_x="left",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="lives",
            icon_name="heart_hud",
            x=VHud.OFFSET + self.maze.width - VData.SPRITE_SIZE * 2.5,
            anchor_x="right",
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="timer",
            icon_name=None,
            x=VHud.OFFSET + self.maze.width / 2,
            anchor_x="center",
            color=self.atlas.get_color("hud_font"),
        )
        self.add_field(
            entry_name="fps",
            icon_name=None,
            x=VHud.OFFSET + self.maze.width / 4,
            anchor_x="center",
            color=self.atlas.get_color("hud_font_debug"),
            debug=True,
        )

    # ########################################################################
    # ######################################################### ADD FIELD ####
    def add_field(
        self,
        x: float,
        anchor_x: str,
        color: Color,
        entry_name: str,
        icon_name: str | None,
        debug: bool = False,
    ) -> None:
        # Field --
        container = self.fields_debug if debug else self.fields
        container[entry_name] = Text(
            text="Hello",
            align=anchor_x,
            anchor_x=anchor_x,
            anchor_y="center",
            font_size=self.atlas.font_size,
            font_name=self.atlas.font_name,
            x=x,
            y=self.y_text_line + 2,
            color=color,
        )

        # Icon --
        text_width = container[entry_name].content_width
        if icon_name:
            match anchor_x:
                case "left":
                    x = x - VData.SPRITE_SIZE / 1.3
                case "center":
                    x = x - text_width / 2 - VData.SPRITE_SIZE
                case _:
                    x = x + VData.SPRITE_SIZE / 1.3

            tile = self.atlas.pick_tile(icon_name)
            self.icons.append(
                self.atlas.tile_to_sprite(
                    tile,
                    Vec2(x, self.y_text_line - 2),
                )
            )

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.background.draw()
        self.frame.draw()
        self.icons.draw(pixelated=True)

        self.fields["score"].text = self.gamestate.score
        self.fields["lives"].text = f"{self.gamestate.lives:>2}"
        self.fields["timer"].text = self.get_time_left()

        for text in self.fields.values():
            text.draw()

        # Debug --
        if VData.debug_on:
            self.fields_debug["fps"].text = f"FPS: {arcade.get_fps():.2f}"
            for text in self.fields_debug.values():
                text.draw()

    # ########################################################################
    # ##################################################### GET TIME LEFT ####
    def get_time_left(self) -> str:
        time_spend = time.time() - self.gamestate.time_start
        time_left = VData.time_max - time_spend

        minutes = int(time_left) // 60
        seconds = int(time_left) % 60

        if minutes < 0:
            return "OVER"
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
