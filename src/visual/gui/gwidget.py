from abc import ABC, abstractmethod

from arcade import Vec2


class GWidget(ABC):
    def update(self, delta_time: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        pass

    def on_enter_key(self) -> None:
        pass

    @property
    @abstractmethod
    def left(self) -> float:
        ...

    @property
    @abstractmethod
    def right(self) -> float:
        ...

    @property
    @abstractmethod
    def position(self) -> Vec2:
        ...

    @position.setter
    @abstractmethod
    def position(self, value: Vec2) -> None:
        ...

    @property
    @abstractmethod
    def center(self) -> float:
        ...
