import arcade
from arcade import Sprite, Vec2, key

from src.visual.vatlas import VAtlas
from src.visual.sprites.swall import SWall
from src.visual.entities.ventity_moving import VEntityMoving


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀█░█░░░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░█▀▀░█░░░█▀█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
class VEntityPlayer(VEntityMoving):
    def __init__(
        self,
        atlas: VAtlas,
        position: Vec2,
        walls: SWall,
    ) -> None:
        super().__init__(atlas, "player", position)
        self.walls: SWall = walls
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        # TODO: Deal with magic number - in the config ? or VData ?
        self.speed = 10

        self.pressed_keys: set[int] = set()
        self.valid_keys: set[int] = {key.UP, key.DOWN, key.LEFT, key.RIGHT}

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_velocity()
        self.update_texture()
        self.resolve_wall_collisions()

    # ########################################################################
    # ########################################################## VELOCITY ####
    def update_velocity(self) -> None:
        """Update player movement based on pressed keys"""

        self.change_x = 0
        self.change_y = 0

        if key.LEFT in self.pressed_keys:
            self.change_x = -1 * self.speed
        if key.RIGHT in self.pressed_keys:
            self.change_x = 1 * self.speed
        if key.UP in self.pressed_keys:
            self.change_y = 1 * self.speed
        if key.DOWN in self.pressed_keys:
            self.change_y = -1 * self.speed

    # ########################################################################
    # ######################################################## COLLISIONS ####
    def resolve_wall_collisions(self) -> None:
        # Resolve movement per-axis to avoid corner tunneling
        # and multi-wall phasing.
        self.center_x += self.change_x
        collided_x: list[Sprite] = arcade.check_for_collision_with_list(
            self, self.walls.sprites
        )
        if self.change_x > 0:
            for wall in collided_x:
                self.right = min(self.right, wall.left)
        elif self.change_x < 0:
            for wall in collided_x:
                self.left = max(self.left, wall.right)

        self.center_y += self.change_y
        collided_y: list[Sprite] = arcade.check_for_collision_with_list(
            self, self.walls.sprites
        )
        if self.change_y > 0:
            for wall in collided_y:
                self.top = min(self.top, wall.bottom)
        elif self.change_y < 0:
            for wall in collided_y:
                self.bottom = max(self.bottom, wall.top)

    # ########################################################################
    # ############################################################ ON KEY ####
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in self.valid_keys:
            self.pressed_keys.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol in self.valid_keys:
            self.pressed_keys.discard(symbol)
