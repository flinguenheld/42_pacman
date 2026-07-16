from src.visual.gui.gui_background import GBackground
import time
import arcade
from arcade.types import Color
from arcade import Text, Vec2, SpriteList

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.vgamestate import VGameState


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

        self.background = GBackground(
            atlas, VHud.OFFSET, VHud.OFFSET, maze.width, VData.SPRITE_SIZE * 3
        )
        self.icons: SpriteList = arcade.SpriteList()
        self.fields_debug: dict[str, Text] = dict()
        self.fields: dict[str, Text] = dict()

        self.build_fields()

    # ########################################################################
    # ############################################################# SETUP ####
    def build_fields(self) -> None:
        self.font_size = VData.SPRITE_SIZE * 0.6
        self.y_text_line = VHud.OFFSET + VData.SPRITE_SIZE / 1.5

        self.add_field(
            entry_name="score",
            icon_name="score_hud",
            x=VHud.OFFSET + VData.SPRITE_SIZE,
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="lives",
            icon_name="heart_hud",
            x=VHud.OFFSET + self.maze.width - VData.SPRITE_SIZE * 3.5,
            color=self.atlas.get_color("hud_font"),
        )

        self.add_field(
            entry_name="timer",
            icon_name=None,
            x=VHud.OFFSET + self.maze.width / 2 - self.font_size * 4,
            color=self.atlas.get_color("hud_font"),
        )
        self.add_field(
            entry_name="fps",
            icon_name=None,
            x=VHud.OFFSET + self.maze.width / 4 - self.font_size * 4,
            color=self.atlas.get_color("hud_font_debug"),
            debug=True,
        )

    # ########################################################################
    # ######################################################### ADD FIELD ####
    def add_field(
        self,
        x: float,
        color: Color,
        entry_name: str,
        icon_name: str | None,
        debug: bool = False,
    ) -> None:

        # Icon --
        if icon_name:
            tile = self.atlas.pick_tile(icon_name)
            self.icons.append(
                self.atlas.tile_to_sprite(
                    tile,
                    Vec2(
                        x + VData.SPRITE_SIZE / 2,
                        self.y_text_line + VData.SPRITE_SIZE / 4,
                    ),
                )
            )

        # Field --
        container = self.fields_debug if debug else self.fields
        container[entry_name] = Text(
            text="Hello",
            x=x + VData.SPRITE_SIZE * 1.2,
            y=self.y_text_line,
            font_size=self.font_size,
            color=color,
            bold=True,
        )

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.background.draw()
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
        self.background.update(delta_time)
        self.icons.update_animation(delta_time)

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self) -> Vec2:
        return self.background.center_position
