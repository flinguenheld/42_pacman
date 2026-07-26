from typing import Literal

import arcade
from arcade import Sprite, SpriteList, Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity import VEntity


type EntityDirection = Literal["wait", "top", "right", "bot", "left"]


# ░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▄█░█▀█░█░█░█▀▀░█▄█░█▀▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█░█░█░█░▀▄▀░█▀▀░█░█░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░
class VEntityMoving(VEntity):
    """
    Add movement options to VEntity
    The Atlas has to contain 5 animated textures:
       - {sprite_name}_wait
       - {sprite_name}_top
       - {sprite_name}_right
       - {sprite_name}_bot
       - {sprite_name}_left
    """

    def __init__(
        self, atlas: VAtlas, sprite_name: str, position: Vec2
    ) -> None:
        super().__init__(atlas, sprite_name, position)

        # Texture helpers --
        self._current_direction: EntityDirection = "wait"

    def get_direction_from_vector(self, vector: Vec2) -> EntityDirection:
        """
        Takes a non-normalized vector as input and returns the corresponding
        entity direction ("top", "right", "bot", "left").
        If the vector does not correspond to any direction,
        returns "wait".
        """

        # Threshold to avoid detecting small movements.
        # Like an enemy slightly adjusting its position in the maze.
        minimal_threshold = 0.9
        if vector.y > minimal_threshold:
            return "top"
        elif vector.x > minimal_threshold:
            return "right"
        elif vector.y < -minimal_threshold:
            return "bot"
        elif vector.x < -minimal_threshold:
            return "left"
        else:
            return "wait"

    # ########################################################################
    # #################################################### UPDATE TEXTURE ####
    def update_texture(self) -> None:
        """
        Change the texture of the entity based on its current
        movement direction.
        Has to be called at the end of the update method of the entity,
        after the change_x and change_y values have been updated.
        """
        # QUESTION: What do you think of that?
        # I think this is a better approach
        requested_direction = self.get_direction_from_vector(
            Vec2(self.change_x, self.change_y)
        )

        if self._current_direction != requested_direction:
            # print(f"update the animation to {requested_direction}")

            new_tile = self._atlas.textures[
                f"{self._sprite_name}_{requested_direction}"
            ][0]

            if not isinstance(new_tile.texture, arcade.TextureAnimation):
                raise ValueError("The given texture has to be animated.")

            self.animation = new_tile.texture
            self._current_direction = requested_direction

    def get_closest_sprite(self, sprite_list: SpriteList[Sprite]) -> Sprite:
        closest_sprite_result = arcade.get_closest_sprite(self, sprite_list)
        _error_msg = (
            f"Could not find a closest sprite for {self} in {sprite_list}."
        )
        assert closest_sprite_result is not None, _error_msg

        (closest_sprite, _) = closest_sprite_result
        return closest_sprite

    def apply_delta_time(self, speed: float, delta_time: float) -> float:
        multiplier = 500.0
        return speed * multiplier * delta_time
