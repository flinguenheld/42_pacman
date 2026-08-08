import arcade

from src.views.vgame import VGame
from src.views.vpause import VPause
from src.sprites.vatlas import VAtlas
from src.views.vcheats import VCheats
from src.views.vvictory import VVictory
from src.views.vwelcome import VWelcome
from src.data.vdata import VNames, VData
from src.data.gamestate import GameState
from src.views.vgame_over import VGameOver
from src.views.vinstructions import VIinstructions


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

            case VNames.VIEW_GAME_NEXT_LEVEL:
                # list index is 0-indexed, but level_id is 1-indexed
                self.game_state.next_level()
                if self.game_state.level > 10:
                    self.switch_view(VNames.VIEW_VICTORY)
                    return
                self.vgame = VGame(self.atlas, self.game_state)
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
            case VNames.VIEW_CHEATS:
                save_and_show(VCheats(self.atlas, self.game_state))

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
