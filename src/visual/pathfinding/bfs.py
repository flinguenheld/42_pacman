from arcade import Vec2
from termcolor import cprint
from collections import deque
from src.visual.vdata import VData


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀░░░▀▀▀░░
class BFS:
    """
    BFS algorithm,
    From the maze graph {floor point: list of all neighbours},
    a start and a target:

      - Create a buffer {point: -1}
      - Fill the buffer with the 'cost' per floor
      - Extract one of the shortest path
    """

    def __init__(self, graph: dict[Vec2, list[Vec2]]):
        self.graph = graph
        self.buffer: dict[Vec2, int] = dict()
        self.path: list[Vec2] = list()

    # ########################################################################
    # ######################################################### SET COSTS ####
    def set_costs(self, start: Vec2, target: Vec2) -> None:
        """
        Fill the buffer with cost per floor until the target
        has been reached.
        """

        self.buffer = {k: -1 for k in self.graph.keys()}
        self.buffer[start] = 0

        queue = deque([start])
        while queue:
            current = queue.popleft()
            cost = self.buffer[current] + 1

            for neighbour in self.graph[current]:
                if self.buffer[neighbour] == -1:
                    self.buffer[neighbour] = cost
                    queue.append(neighbour)

                    if neighbour == target:
                        return

    # ########################################################################
    # ###################################################### EXTRACT PATH ####
    def extract_path(self, target: Vec2) -> list[Vec2]:
        """Sail back up in the buffer to get the path"""

        self.path = [target]
        while self.buffer[self.path[-1]] != 0:
            neigbours = [
                n for n in self.graph[self.path[-1]] if self.buffer[n] >= 0
            ]
            self.path.append(min(neigbours, key=lambda n: self.buffer[n]))

        self.path.reverse()
        return self.path

    # ########################################################################
    # ###################################################### PRINT DEBUG_ ####
    def print_debug(self) -> None:
        """Print the maze according to the current values in buffer & path."""

        size = VData.SPRITE_SIZE

        # --
        x_max = max(self.graph.keys(), key=lambda k: k.x)
        y_max = max(self.graph.keys(), key=lambda k: k.y)

        for y in range(int(y_max.y) + size, -size, -size):
            for x in range(0, int(x_max.x) + size * 2, size):
                point = Vec2(x, y)

                if point in self.buffer:
                    if self.buffer[point] == -1:
                        cprint(" . ", end="", color="grey")
                    else:
                        colour = "red" if point in self.path else "yellow"
                        cprint(
                            f"{self.buffer[point] % 100:>3}",
                            end="",
                            color=colour,
                        )

                elif point in self.graph.keys():
                    print("   ", end="")
                else:
                    cprint("███", end="", color="grey")

            print()
