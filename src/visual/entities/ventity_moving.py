import arcade
from arcade import Vec2

from src.maze.maze import Maze
from src.visual.vdata import VData
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
        maze: Maze,
        sprite_name: str,
        position: Vec2,
    ) -> None:
        super().__init__(atlas, sprite_name, position)
        self.maze = maze

        # TODO: Confirm that --
        # Used by children to know where they are
        # Has to be updated on after each move
        self.current_floor = self.maze.closest_floor_of(self.center)

        # Texture helpers --
        self._current_direction: str = "wait"

    # ########################################################################
    # ##################################################### GET DIRECTION ####
    def get_direction(self) -> str:
        """
        Takes a non-normalized vector as input and returns the corresponding
        entity direction ("top", "right", "bot", "left").
        If the vector does not correspond to any direction,
        returns "wait".
        """

        # Threshold to avoid detecting small movements.
        # Like an enemy slightly adjusting its position in the maze.
        MINIMAL_THRESHOLD = 0.9
        if self.change_y > MINIMAL_THRESHOLD:
            return "top"
        elif self.change_x > MINIMAL_THRESHOLD:
            return "right"
        elif self.change_y < -MINIMAL_THRESHOLD:
            return "bot"
        elif self.change_x < -MINIMAL_THRESHOLD:
            return "left"
        else:
            return "wait"

    # ########################################################################
    # #################################################### UPDATE TEXTURE ####
    def update_texture(self, force: bool = False) -> None:
        """
        Change the texture of the entity based on its current direction.
        """

        new_dir = self.get_direction()

        if self._current_direction != new_dir or force:
            new_tile = self._atlas.pick_tile(f"{self._sprite_name}_{new_dir}")

            if not isinstance(new_tile.texture, arcade.TextureAnimation):
                raise ValueError("The given texture has to be animated.")

            self.animation = new_tile.texture
            self._current_direction = new_dir

    # ########################################################################
    # ################################################## APPLY DELTA TIME ####
    def apply_delta_time(self, speed: float, delta_time: float) -> float:

        # Magic number used to compensate for the delta time
        # So that you don't need to put absurd values for speed
        # Magic numbers are bad but this one is acceptable
        MULTIPLIER = 500.0
        return speed * MULTIPLIER * delta_time

    # ########################################################################
    # ###################################################### IS IN SPRITE ####
    def is_in_sprite(self, point: Vec2, sprite_center: Vec2) -> bool:
        """
        Return True if the given point is inside the square represented
        by the sprite.
        """

        return (
            point.x >= sprite_center.x - VData.SPRITE_SIZE // 2
            and point.x <= sprite_center.x + VData.SPRITE_SIZE // 2
            and point.y >= sprite_center.y - VData.SPRITE_SIZE // 2
            and point.y <= sprite_center.y + VData.SPRITE_SIZE // 2
        )

    # ########################################################################
    # ################################################# IS IN A NEIGHBOUR ####
    def is_in_a_neigbhour(self, point: Vec2) -> Vec2 | None:
        """
        Get the neighbours of the current floor.
        If the point is inside one of them, return its center.
        Otherwise, return None.
        """

        for n in self.maze.graph_neighbours[self.current_floor]:
            if self.is_in_sprite(point, n):
                return n

        return None
