from src.maze.maze_wrapper import Maze
import arcade
from arcade import Sprite, SpriteList, SpriteSolidColor, Text, Vec2

from src.visual.vdata import VData
from src.visual.vatlas import VAtlas
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
        self.setup()

        self.background = arcade.SpriteList()
        self._build()

    # ########################################################################
    # ############################################################# BUILD ####
    def _build(self):
        self.background.clear()

        def add_sprite(x: int, what: str):
            tile = self.atlas.pick_tile(what)
            sprite = self.atlas.tile_to_sprite(tile, Vec2(x, y))
            self.background.append(sprite)
            return x + VData.SPRITE_SIZE

        def fill_line(x: int, what: str):
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

    def setup(self) -> None:
        self.font_size = VData.SPRITE_SIZE * 0.6
        self._init_hud_text()

        self._init_debug_hud_text()

    def _init_hud_text(self) -> None:

        self.score_text = Text(
            "",
            x=VHud.OFFSET + VData.SPRITE_SIZE,
            y=VHud.OFFSET + VData.SPRITE_SIZE / 1.5,
            color=self.atlas.get_color("hud_font"),
            font_size=self.font_size,
            bold=True,
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
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.background.draw()
        self._draw_hud()

    def _draw_hud(self) -> None:
        self.score_text.text = f"Score: {self.gamestate.score}"
        self.score_text.draw()

    def _draw_debug_hud(self) -> None:
        current_fps = arcade.get_fps()
        self.fps_text.text = f"FPS: {current_fps:.2f}"
        self.fps_text.draw()

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self):
        return Vec2(
            VHud.OFFSET + (self.maze.width / 2),
            VHud.OFFSET + VData.SPRITE_SIZE * 1.5,
        )
