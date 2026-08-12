import arcade

from src.data.enums import VNames
from src.views.vgame import VGame
from src.views.vpause import VPause
from src.config.config import Config
from src.sprites.vatlas import VAtlas
from src.views.vcheats import VCheats
from src.views.vvictory import VVictory
from src.views.vwelcome import VWelcome
from src.data.gamestate import GameState
from src.config.utils import apply_config
from src.views.vgame_over import VGameOver
from src.views.vnext_level import VNextLevel
from src.views.vinstructions import VIinstructions


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░█▀█░▀█▀░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░░█░░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░░
class VMain(arcade.Window):
    def __init__(self, config_path: str) -> None:
        super().__init__(
            Config.window_width,
            Config.window_height,
            "Pac-man",
            resizable=True,
        )

        apply_config(config_path)

        arcade.enable_timings()
        arcade.resources.load_kenney_fonts()

        self.atlas = VAtlas()
        self.atlas.load()

        self.previous_vname = VNames.VIEW_WELCOME
        self.current_vname = VNames.VIEW_WELCOME
        self.switch_view(VNames.VIEW_WELCOME)

    # ########################################################################
    # ####################################################### SWITCH VIEW ####
    def switch_view(self, to: VNames) -> None:
        """
        Used to change the current view.
        Save the previous/current name to deal with VName.PREVIOUS.
        """

        def save_and_show(which: arcade.View) -> None:
            self.previous_vname = self.current_vname
            self.current_vname = to

            self.show_view(which)

        match to:
            case VNames.VIEW_NEW_GAME:
                # --> Init a new game here <--
                self.gamestate = GameState()
                self.vgame = VGame(self.atlas, self.gamestate)
                save_and_show(
                    VNextLevel(
                        self.atlas,
                        self.gamestate.level,
                    )
                )
            case VNames.VIEW_GAME_RESUME:
                save_and_show(self.vgame)
            case VNames.VIEW_GAME_NEW_LEVEL:
                self.vgame = VGame(self.atlas, self.gamestate)
                save_and_show(self.vgame)
            case VNames.VIEW_GAMEOVER:
                save_and_show(VGameOver(self.atlas, self.gamestate.score))
            case VNames.VIEW_INSTRUCTIONS:
                save_and_show(VIinstructions(self.atlas))
            case VNames.VIEW_PAUSE:
                save_and_show(VPause(self.atlas))
            case VNames.VIEW_NEXT_LEVEL:
                if self.gamestate.level >= Config.amount_of_levels:
                    self.switch_view(VNames.VIEW_VICTORY)
                else:
                    self.gamestate.next_level()
                    save_and_show(
                        VNextLevel(
                            self.atlas,
                            self.gamestate.level,
                        )
                    )
            case VNames.VIEW_WELCOME:
                save_and_show(VWelcome(self.atlas))
            case VNames.VIEW_VICTORY:
                save_and_show(VVictory(self.atlas, self.gamestate.score))
            case VNames.VIEW_CHEATS:
                save_and_show(VCheats(self.atlas, self.gamestate))

            # --
            case VNames.VIEW_PREVIOUS:
                if self.previous_vname == VNames.VIEW_NEW_GAME:
                    self.switch_view(VNames.VIEW_GAME_RESUME)
                else:
                    self.switch_view(self.previous_vname)

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        Config.window_width = width
        Config.window_height = height
