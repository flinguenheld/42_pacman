import arcade
from arcade.types import Point2

from src.visual import VData
from arcade.hitbox import HitBox
from arcade import Sprite, Vec2, key
from src.visual.sprites.swall import SWall
from src.visual.vgamestate import GameState


class Player(Sprite):
    def __init__(
        self, start_pos: Point2, walls: SWall, gamestate: GameState
    ) -> None:
        super().__init__(
            VData.TEXTURES + "/hen.png",
            scale=0.3,
            center_x=start_pos[0],
            center_y=start_pos[1],
        )
        self.speed: int = 10
        self.walls: SWall = walls
        self.gamestate: GameState = gamestate

        hitbox_scale: float = 0.50
        half_w: float = self.width / 2
        half_h: float = self.height / 2
        self.hit_box = HitBox(
            points=[
                (-half_w, -half_h),
                (half_w, -half_h),
                (half_w, half_h),
                (-half_w, half_h),
            ],
            position=self.position,
            scale=Vec2(hitbox_scale, hitbox_scale),
        )
        self.pressed_keys: set[int] = set()
        self.valid_keys: set[int] = {key.UP, key.DOWN, key.LEFT, key.RIGHT}

    def update(self, delta_time: float = 1 / 60) -> None:
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

        # Resolve movement per-axis to avoid corner
        # tunneling and multi-wall phasing.
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
