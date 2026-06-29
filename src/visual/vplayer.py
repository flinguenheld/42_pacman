import arcade

from src.visual import VData
from arcade.hitbox import HitBox
from arcade import Sprite, Vec2, key
from src.visual.sprites.swall import SWall
from src.utils.maze_grid_to_world_coords import maze_grid_to_world_coords


class Player(Sprite):
    def __init__(self, start_pos: Vec2, walls: SWall) -> None:
        center = start_pos - (VData.SPRITE_SIZE / 2)
        super().__init__(
            VData.TEXTURES + "/hen.png",
            scale=0.3,
            center_x=center.x,
            center_y=center.y,
        )
        self.speed: int = 10
        self.walls: SWall = walls

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

    def update(self, delta_time: float = 1 / 60) -> None:
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
        # Handle player movement based on key presses
        match symbol:
            case key.LEFT:
                self.change_x = -1 * self.speed
            case key.RIGHT:
                self.change_x = 1 * self.speed
            case key.UP:
                self.change_y = 1 * self.speed
            case key.DOWN:
                self.change_y = -1 * self.speed
            case _:
                pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        # Stop player movement when keys are released
        match symbol:
            case key.LEFT | key.RIGHT:
                self.change_x = 0
            case key.UP | key.DOWN:
                self.change_y = 0
            case _:
                pass
