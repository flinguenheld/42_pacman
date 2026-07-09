from abc import ABC

from arcade import Sprite, Vec2


class VEntity(ABC):
    def __init__(self, position: Vec2):
        self.sprite: Sprite | None = None
        self._position: Vec2 = position

        self._change_x: float = 0
        self._change_y: float = 0

        self.setup()

    def setup(self) -> None:
        pass

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, value: Vec2) -> None:
        if self.sprite:
            self.sprite.position = value
        self._position = value

    @property
    def change_x(self) -> float:
        return self._change_x

    @change_x.setter
    def change_x(self, value: float) -> None:
        if self.sprite:
            self.sprite.change_x = value
        self._change_x = value

    @property
    def change_y(self) -> float:
        return self._change_y

    @change_y.setter
    def change_y(self, value: float) -> None:
        if self.sprite:
            self.sprite.change_y = value
        self._change_y = value

    def update(self, delta_time: float = 1 / 60) -> None:
        pass

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.sprite:
            self.sprite.update_animation(delta_time)

    def set_sprite(self, sprite: Sprite | None) -> None:
        if sprite is None:
            self.sprite = None
            return
        else:
            sprite.position = self.position
            self.sprite = sprite

    def on_up_movement(self) -> None:
        pass

    def on_down_movement(self) -> None:
        pass

    def on_left_movement(self) -> None:
        pass

    def on_right_movement(self) -> None:
        pass
