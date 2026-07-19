from src.visual.vdata import VData
from arcade import Vec2, Text, SpriteList
from src.visual.vatlas import VAtlas


class GEntry:
    def __init__(self, atlas: VAtlas, text: str, center: Vec2):

        self.atlas = atlas
        self.active = False

        # Text --
        self.text = Text(
            text=text,
            x=center.x,
            y=center.y,
            font_name=self.atlas.font_name,
            font_size=self.atlas.font_size,
            align="center",
            anchor_x="center",
            anchor_y="center",
            color=atlas.get_color("menu_font"),
        )

        # Icons --
        shift = self.text.content_width / 2 + VData.SPRITE_SIZE

        self.icons = SpriteList()
        tile = self.atlas.pick_tile("player_wait")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(center.x - shift, center.y - 5),
            )
        )

        tile = self.atlas.pick_tile("player_wait")
        self.icons.append(
            self.atlas.tile_to_sprite(
                tile,
                Vec2(center.x + shift, center.y - 5),
            )
        )

    # ########################################################################
    # ##################################################### TOGGLE ACTIVE ####
    def set_active(self, value: bool) -> None:
        self.active = value

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.text.draw()

        if self.active:
            self.icons.draw(pixelated=True)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.icons.update_animation(delta_time)


class GMenu:
    def __init__(
        self,
        atlas: VAtlas,
        choices: list[str],
        center_top_first: Vec2,
    ):
        self.atlas = atlas

        self.choices = []

        for choice in choices:
            new_entry = GEntry(self.atlas, choice, center=center_top_first)
            center_top_first -= Vec2(0, VData.FONT_SIZE * 1.6)
            self.choices.append(new_entry)

    # ########################################################################
    # ############################################################## NEXT ####
    def next_up(self):
        pass

    def next_down(self):
        pass

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self):
        for choice in self.choices:
            choice.draw()

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        for choice in self.choices:
            choice.update(delta_time)
