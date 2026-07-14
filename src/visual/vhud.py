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

        self.background: SpriteList = arcade.SpriteList()
        self.icons: SpriteList = arcade.SpriteList()
        self.fields_debug: dict[str, Text] = dict()
        self.fields: dict[str, Text] = dict()

        self.build_background()
        self.build_fields()

    # ########################################################################
    # ############################################################# BUILD ####
    def build_background(self) -> None:
        def add_sprite(x: int, what: str) -> int:
            tile = self.atlas.pick_tile(what)
            sprite = self.atlas.tile_to_sprite(tile, Vec2(x, y))
            self.background.append(sprite)
            return x + VData.SPRITE_SIZE

        def fill_line(x: int, what: str) -> int:
            while x < VHud.OFFSET + self.maze.width:
                add_sprite(x, what)
                x += VData.SPRITE_SIZE
            return x

        # --
        base_wall = "wall_with_floor_on_"
        extra = "wall_extra_corner_"

        y = VHud.OFFSET
        x = VHud.OFFSET
        x = add_sprite(x, f"{extra}top_right")
        x = fill_line(x, f"{base_wall}top")
        add_sprite(x, f"{extra}top_left")

        y += VData.SPRITE_SIZE
        x = VHud.OFFSET
        x = add_sprite(x, f"{base_wall}right")
        x = fill_line(x, "floor_hud")
        add_sprite(x, f"{base_wall}left")

        y += VData.SPRITE_SIZE
        x = VHud.OFFSET
        x = add_sprite(x, f"{extra}bot_right")
        x = fill_line(x, f"{base_wall}bottom")
        add_sprite(x, f"{extra}bot_left")

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
        self.background.draw(pixelated=True)
        self.icons.draw(pixelated=True)

        self.fields["score"].text = self.gamestate.score
        self.fields["lives"].text = f"{self.gamestate.lives:>2}"
        self.fields["timer"].text = "42:42"

        for text in self.fields.values():
            text.draw()

        # Debug --
        if VData.debug_on:
            self.fields_debug["fps"].text = f"FPS: {arcade.get_fps():.2f}"
            for text in self.fields_debug.values():
                text.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.background.update_animation(delta_time)
        self.icons.update_animation(delta_time)

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self) -> Vec2:
        return Vec2(
            VHud.OFFSET + (self.maze.width / 2),
            VHud.OFFSET + VData.SPRITE_SIZE * 1.5,
        )
