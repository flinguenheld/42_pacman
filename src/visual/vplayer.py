from src.visual.vatlas import VAtlas
import arcade

from arcade import Sprite, Vec2, key
from src.visual.entities.ventity import VEntityMovement
from src.visual.sprites.swall import SWall
from src.visual.vgamestate import GameState


class VPlayerEntity(VEntityMovement):
    def __init__(
        self,
        atlas: VAtlas,
        sprite_name: str,
        position: Vec2,
        walls: SWall,
        gamestate: GameState,
    ):
        super().__init__(atlas, sprite_name, position)
        self.walls: SWall = walls
        self.gamestate: GameState = gamestate

    def setup(self) -> None:
        self.speed = 10

        self.pressed_keys: set[int] = set()
        self.valid_keys: set[int] = {key.UP, key.DOWN, key.LEFT, key.RIGHT}

        # self.sprite = VSpriteEntity()
        # self.set_sprite("player")

    def update(self, delta_time: float = 1 / 60) -> None:
        self.update_velocity()
        self.resolve_collisions()

    def update_velocity(self) -> None:
        # Update player movement based on pressed keys
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

    def resolve_collisions(self) -> None:
        if not self.sprite:
            return
        # Resolve movement per-axis to avoid corner tunneling
        # and multi-wall phasing.
        self.sprite.center_x += self.change_x
        collided_x: list[Sprite] = arcade.check_for_collision_with_list(
            self.sprite, self.walls.sprites
        )
        if self.change_x > 0:
            for wall in collided_x:
                self.sprite.right = min(self.sprite.right, wall.left)
        elif self.change_x < 0:
            for wall in collided_x:
                self.sprite.left = max(self.sprite.left, wall.right)

        self.sprite.center_y += self.change_y
        collided_y: list[Sprite] = arcade.check_for_collision_with_list(
            self.sprite, self.walls.sprites
        )
        if self.change_y > 0:
            for wall in collided_y:
                self.sprite.top = min(self.sprite.top, wall.bottom)
        elif self.change_y < 0:
            for wall in collided_y:
                self.sprite.bottom = max(self.sprite.bottom, wall.top)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Handle key press events to control player movement
        if symbol not in self.valid_keys:
            return
        self.pressed_keys.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        # Handle key release events to stop player movement
        if symbol not in self.valid_keys:
            return
        self.pressed_keys.discard(symbol)
