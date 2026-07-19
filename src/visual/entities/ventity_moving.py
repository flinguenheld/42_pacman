import arcade
from arcade import Sprite, SpriteList, Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity import VEntity


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
        self._change_x = 0.0
        self._change_y = 0.0

        # Texture helpers --
        self._current_direction = "wait"
        self._requested_direction = "wait"

    # ########################################################################
    # #################################################### UPDATE TEXTURE ####
    def update_texture(self) -> None:
        """
        Change the animation according to the request.
        Avoid useless changes.
        Has to be called after 'change_x' and 'change_y' updates.
        """
        # TODO: Maybe replace this whole system of setting
        # a requested direction and then updating the texture
        # with a more direct approach?
        # Like removing the change_x and change_y properties
        # and just compute the direction based on these values in this method.
        # This is just an idea
        if self._current_direction != self._requested_direction:
            # print(f"up the animation to {self._requested_direction}")

            new_tile = self._atlas.textures[
                f"{self._sprite_name}_{self._requested_direction}"
            ][0]

            if not isinstance(new_tile.texture, arcade.TextureAnimation):
                raise ValueError("The given texture has to be animated.")

            self.animation = new_tile.texture
            self._current_direction = self._requested_direction

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

    # ########################################################################
    # ########################################################## CHANGE X ####
    @property
    def change_x(self) -> float:
        return self._change_x

    @change_x.setter
    def change_x(self, new_value: float) -> None:

        if new_value != self.change_x:
            match new_value:
                case 0:
                    self._requested_direction = "wait"
                case v if v > 0:
                    self._requested_direction = "right"
                case _:
                    self._requested_direction = "left"

            self._change_x = new_value

    # ########################################################################
    # ########################################################## CHANGE Y ####
    @property
    def change_y(self) -> float:
        return self._change_y

    @change_y.setter
    def change_y(self, new_value: float) -> None:
        if new_value != self.change_y:
            match new_value:
                case 0:
                    self._requested_direction = "wait"
                case v if v > 0:
                    self._requested_direction = "top"
                case _:
                    self._requested_direction = "bot"

            self._change_y = new_value
