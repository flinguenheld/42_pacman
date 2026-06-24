from arcade import Sprite, Vec2, key

from src.visual import VData

class Player(Sprite):
    def __init__(self) -> None:
        super().__init__(
            VData.SPRITES + "/hen.png",
            scale=1,
            center_x=150,
            center_y=150,
            )
        self.speed = 10

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Handle player movement based on key presses
        match symbol:
            case key.LEFT:
                self.velocity = Vec2(-1 * self.speed, 0)
            case key.RIGHT:
                self.velocity = Vec2(1 * self.speed, 0)
            case key.UP:
                self.velocity = Vec2(0, 1 * self.speed)
            case key.DOWN:
                self.velocity = Vec2(0, -1 * self.speed)
            case _:
                pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.angle += 10  # Rotate the player when keys are released
        # Stop player movement when keys are released
        match symbol:
            case key.LEFT | key.RIGHT:
                self.velocity = Vec2(0, 0)
            case key.UP | key.DOWN:
                self.velocity = Vec2(0, 0)
            case _:
                pass
