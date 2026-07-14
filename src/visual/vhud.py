import arcade
from arcade import Text, Vec2, SpriteList
from arcade.types import Color

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.vgamestate import VGameState


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
        self.texts: dict[str, Text] = dict()

        self.setup()
        self.build()

    # ########################################################################
    # ############################################################# BUILD ####
    def build(self) -> None:
        self.background.clear()

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
    def setup(self) -> None:
        self.font_size = VData.SPRITE_SIZE * 0.6
        self.y_text_line = VHud.OFFSET + VData.SPRITE_SIZE / 1.5
        self._init_hud_text()

        self._init_debug_hud_text()

    def _init_hud_text(self) -> None:
        self.icons.clear()
        self.texts.clear()

        self.add_text(
            "score",
            "pacgum_wait",
            VHud.OFFSET + VData.SPRITE_SIZE,
            self.atlas.get_color("hud_font"),
        )

        self.add_text(
            "lives",
            "player_wait",
            VHud.OFFSET + self.maze.width - VData.SPRITE_SIZE * 3.5,
            self.atlas.get_color("hud_font"),
        )

    def _init_debug_hud_text(self) -> None:

        self.fps_text = Text(
            "",
            x=10,
            y=0,
            color=arcade.color.WHITE,
            font_size=self.font_size,
            bold=True,
        )

    # ########################################################################
    # ########################################################## ADD TEXT ####
    def add_text(
        self,
        entry_name: str,
        icon_name: str,
        x: float,
        color: Color,
        debug: bool = False,
    ) -> None:
        sprite_size = VData.SPRITE_SIZE

        tile = self.atlas.pick_tile(icon_name)
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(x + sprite_size / 2, self.y_text_line + sprite_size / 4),
            )
        )

        self.texts[entry_name] = Text(
            "Hello",
            x=x + VData.SPRITE_SIZE * 1.2,
            y=self.y_text_line,
            color=color,
            font_size=self.font_size,
            bold=True,
        )

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.background.draw(pixelated=True)
        self.icons.draw(pixelated=True)

        self.texts["score"].text = self.gamestate.score
        self.texts["lives"].text = f"{self.gamestate.lives:>2}"

        for text in self.texts.values():
            text.draw()

    def _draw_debug_hud(self) -> None:
        current_fps = arcade.get_fps()
        self.fps_text.text = f"FPS: {current_fps:.2f}"
        self.fps_text.draw()

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
