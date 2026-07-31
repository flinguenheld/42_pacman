import arcade

from src.visual.vgame import VGame
from src.visual.vatlas import VAtlas
from src.visual.vdata import VNames, VData
from src.visual.views.vcheat import VCheat
from src.visual.views.vpause import VPause
from src.visual.gamestate import GameState
from src.visual.views.vvictory import VVictory
from src.visual.views.vwelcome import VWelcome
from src.visual.views.vgame_over import VGameOver
from src.visual.views.vinstructions import VIinstructions


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▄█░█▀█░▀█▀░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█░█░█▀█░░█░░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░░
class VMain(arcade.Window):
    def __init__(self) -> None:
        super().__init__(
            VData.width,
            VData.height,
            "Pac-man",
            resizable=True,
        )

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
            case VNames.VIEW_GAME_NEW:
                # --> Init a new game here <--
                self.game_state = GameState()
                self.vgame = VGame(self.atlas, self.game_state)
                save_and_show(self.vgame)

            case VNames.VIEW_GAME_RESUME:
                save_and_show(self.vgame)

            case VNames.VIEW_GAMEOVER:
                save_and_show(VGameOver(self.atlas, self.game_state.score))
            case VNames.VIEW_INSTRUCTIONS:
                save_and_show(VIinstructions(self.atlas))
            case VNames.VIEW_PAUSE:
                save_and_show(VPause(self.atlas))
            case VNames.VIEW_WELCOME:
                save_and_show(VWelcome(self.atlas))
            case VNames.VIEW_VICTORY:
                save_and_show(VVictory(self.atlas, self.game_state.score))
            case VNames.VIEW_CHEAT:
                save_and_show(VCheat(self.atlas, self.game_state))
            # --
            case VNames.VIEW_PREVIOUS:
                if self.previous_vname == VNames.VIEW_GAME_NEW:
                    self.switch_view(VNames.VIEW_GAME_RESUME)
                else:
                    self.switch_view(self.previous_vname)

    # ########################################################################
    # ######################################################### ON RESIZE ####
    def on_resize(self, width: int, height: int) -> None:
        VData.width = width
        VData.height = height
