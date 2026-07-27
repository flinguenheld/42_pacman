import arcade
from arcade import Vec2

from src.visual.vatlas import VAtlas
from src.visual.entities.ventity import VEntity


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▄█░█▀█░█░█░▀█▀░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█░█░█░█░▀▄▀░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░░
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
        self,
        atlas: VAtlas,
        sprite_name: str,
        position: Vec2,
    ) -> None:
        super().__init__(atlas, sprite_name, position)

        # Texture helpers --
        self._current_direction: str = "wait"

    # ########################################################################
    # ##################################################### GET DIRECTION ####
    def get_direction(self, vector: Vec2) -> str:
        """
        Takes a non-normalized vector as input and returns the corresponding
        entity direction ("top", "right", "bot", "left").
        If the vector does not correspond to any direction,
        returns "wait".
        """

        # Threshold to avoid detecting small movements.
        # Like an enemy slightly adjusting its position in the maze.
        MINIMAL_THRESHOLD = 0.9
        if vector.y > MINIMAL_THRESHOLD:
            return "top"
        elif vector.x > MINIMAL_THRESHOLD:
            return "right"
        elif vector.y < -MINIMAL_THRESHOLD:
            return "bot"
        elif vector.x < -MINIMAL_THRESHOLD:
            return "left"
        else:
            return "wait"

    # ########################################################################
    # #################################################### UPDATE TEXTURE ####
    def update_texture(self) -> None:
        """
        Change the texture of the entity based on its current direction.
        """

        new_dir = self.get_direction(Vec2(self.change_x, self.change_y))

        if self._current_direction != new_dir:
            new_tile = self._atlas.pick_tile(f"{self._sprite_name}_{new_dir}")

            if not isinstance(new_tile.texture, arcade.TextureAnimation):
                raise ValueError("The given texture has to be animated.")

            self.animation = new_tile.texture
            self._current_direction = new_dir

    # ########################################################################
    # ################################################## APPLY DELTA TIME ####
    def apply_delta_time(self, speed: float, delta_time: float) -> float:

        # QUESTION: What is that number ?
        # QUESTION: Should it be managed somewhere else like Config or VData ?
        multiplier = 500.0
        return speed * multiplier * delta_time
