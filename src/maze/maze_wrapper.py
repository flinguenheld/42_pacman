from dataclasses import dataclass, field

from arcade import Vec2
from mazegenerator import MazeGenerator


@dataclass
class Maze:
    seed: int = 42
    size: Vec2 = Vec2(15, 15)
    maze: set[Vec2] = field(default_factory=set)

    def generate_new_maze(self) -> None:
        raw_maze = MazeGenerator(
            size=(int(self.size.x), int(self.size.y)),
            perfect=False,
            seed=self.seed,
        ).maze

        for y, column in enumerate(self.maze):
            for x, row in enumerate(column):
                pass
