from arcade import Vec2, Text

from src.visual.vdata import VNames
from src.visual.vatlas import VAtlas
from src.visual.gui.gmenu import GMenu
from src.visual.gui.gframe import GFrame
from src.visual.gui.gwindow import GWindow
from src.visual.gui.gmenu_entry import GMenuEntry
from src.visual.gui.titles.gtitle_instructions import GTitleInstructions


class VIinstructions(GWindow):
    def __init__(self, atlas: VAtlas) -> None:
        super().__init__(
            atlas,
            title=GTitleInstructions(atlas),
            frame=GFrame(
                atlas=atlas,
                nb_rows=35,
                nb_cols=43,
                bevels=True,
            ),
        )

        # --
        self.menu = GMenu(
            atlas=self.atlas,
            choices={
                "OK": GMenuEntry.ToCall(
                    func=self.window.switch_view,
                    args=[VNames.VIEW_PREVIOUS],
                ),
            },
            center_top_first=Vec2(self.frame.center_position.x, 100),
        )

        self.to_draw_and_update.append(self.menu)

        # --
        self.text = Text(
            text=self.instructions(),
            x=self.frame.center_position.x,
            y=self.frame.center_position.y,
            font_name=self.atlas.font_name,
            font_size=self.atlas.font_size,
            align="center",
            anchor_x="center",
            anchor_y="center",
            color=atlas.get_color("menu_font"),
        )

        self.to_draw_and_update.append(self.text)

    # ########################################################################
    # ############################################################# SETUP ####
    def instructions(self) -> str:

        txt = "blah blah blah"

        return txt

    # ########################################################################
    # ############################################################## KEYS ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.menu.key_press(symbol)
