from arcade import Sprite, SpriteList, SpriteSolidColor, Text
import arcade

from src.visual.vdata import VData
from src.visual.vgamestate import VGameState


class VHud:
    """
    Class representing the HUD (Heads-Up Display) in the game.
    """

    def __init__(self, gamestate: VGameState) -> None:
        self.gamestate = gamestate
        self.setup()

    def setup(self) -> None:
        """
        Sets up the HUD elements, such as score and FPS display.
        """
        self.bg_sprite_list: SpriteList[Sprite] = SpriteList()

        self._init_hud_bg()
        self._init_hud_text()

        self._init_debug_hud_text()

    def _init_hud_bg(self) -> None:
        """
        Initializes the background sprite for the HUD.
        """
        self.hud_bg_sprite = SpriteSolidColor(
            width=VData.width,
            height=55,
            color=arcade.color.BLACK,
        )
        self.hud_bg_sprite.center_x = VData.width / 2
        self.hud_bg_sprite.center_y = VData.height - (
            self.hud_bg_sprite.height / 2
        )
        self.bg_sprite_list.append(self.hud_bg_sprite)

    def _init_hud_text(self) -> None:
        """
        Initializes the text object for displaying the score.
        """
        self.score_text = Text(
            f"Score: {self.gamestate.score}",
            x=10,
            y=VData.height - 30,
            color=arcade.color.WHITE,
            font_size=22,
            bold=True,
        )

    def _init_debug_hud_text(self) -> None:
        """
        Initializes the text object for displaying debug information,
        such as FPS.
        """
        self.fps_text = Text(
            f"FPS: {arcade.get_fps():.2f}",
            x=10,
            y=0,
            color=arcade.color.WHITE,
            font_size=22,
            bold=True,
        )

    def draw(self) -> None:
        """
        Draws the HUD elements on the screen.
        """
        self._draw_hud()
        self._draw_debug_hud()

    def _draw_hud(self) -> None:
        """
        Draws the main HUD elements, such as score and lives.
        """
        self.bg_sprite_list.draw()

        current_score = self.gamestate.score
        self.score_text.text = f"Score: {current_score}"
        self.score_text.draw()

    def _draw_debug_hud(self) -> None:
        """
        Draws debug information on the screen, such as FPS.
        """
        current_fps = arcade.get_fps()
        self.fps_text.text = f"FPS: {current_fps:.2f}"
        self.fps_text.draw()
