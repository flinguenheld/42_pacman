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
        closest_wall: Sprite | None = None
        closest_distance: float = float("inf")
        for wall in collided:
            distance: float = arcade.get_distance_between_sprites(self, wall)
            if distance < closest_distance:
                closest_distance = distance
                closest_wall = wall

        if closest_wall is not None:
            # Calculate the overlap between the player and the closest wall
            overlap_x: float = (self.width / 2 + closest_wall.width / 2) - abs(self.center_x - closest_wall.center_x)
            overlap_y: float = (self.height / 2 + closest_wall.height / 2) - abs(self.center_y - closest_wall.center_y)

            # Resolve the collision by moving the player out of the wall
            if overlap_x < overlap_y:
                if self.center_x < closest_wall.center_x:
                    self.center_x -= overlap_x
                else:
                    self.center_x += overlap_x
            else:
                if self.center_y < closest_wall.center_y:
                    self.center_y -= overlap_y
                else:
                    self.center_y += overlap_y


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
