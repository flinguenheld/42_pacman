from arcade import Sprite, Vec2, key
import arcade

from src.visual import VData
from src.visual.sprites.swall import SWall


class Player(Sprite):
    def __init__(self, start_pos: Vec2, walls: SWall) -> None:
        super().__init__(
            VData.SPRITES + "/hen.png",
            scale=0.3,
            center_x=start_pos.x * VData.SPRITE_SIZE
            + VData.SPRITE_SHIFT,
            center_y=start_pos.y * VData.SPRITE_SIZE
            + VData.SPRITE_SHIFT,
        )
        self.speed: int = 10
        self.walls: SWall = walls

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)
        collided: list[Sprite] = arcade.check_for_collision_with_list(self, self.walls.sprites)

        for wall in collided:
            if self.change_x > 0:  # Moving right; Hit the left side of the wall
                self.right = wall.left
            elif self.change_x < 0:  # Moving left; Hit the right side of the wall
                self.left = wall.right
            elif self.change_y > 0:  # Moving up; Hit the bottom side of the wall
                self.top = wall.bottom
            elif self.change_y < 0:  # Moving down; Hit the top side of the wall
                self.bottom = wall.top

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
