from arcade import Vec2
from src.visual.vatlas import VAtlas
from src.visual.sprites.sprites import Sprites


class SBackground(Sprites):
    def __init__(self, atlas: VAtlas) -> None:
        # TODO: CHANGE NAME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TODO: CHANGE NAME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TODO: CHANGE NAME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TODO: CHANGE NAME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        super().__init__(atlas, "wall_")

    def reload(self, backgrounds: set[Vec2]) -> None:

        self.clear()
        for point in backgrounds:
            self.add_sprite(
                f"{self.base_name}open_full",
                center=point,
                to_world_coordinates=False,
            )
