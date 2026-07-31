import sys
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

      - Create a buffer {point: sys.maxsize}
      - Fill the buffer with the 'cost' per floor
      - Extract one of the shortest path
    """

    NOT_VISITED = sys.maxsize

    def __init__(self, graph_neighbours: dict[Vec2, list[Vec2]]):
        self.graph_neighbours = graph_neighbours

    # ########################################################################
    # ######################################################### SET COSTS ####
    def set_costs(self, start: Vec2) -> dict[Vec2, int]:
        """
        Fill and return a dict with the cost per floor according to
        the start position.
        """

        graph_costs = dict.fromkeys(self.graph_neighbours, BFS.NOT_VISITED)
        graph_costs[start] = 0

        queue = deque([start])
        while queue:
            current = queue.popleft()
            cost = graph_costs[current] + 1

            for neighbour in self.graph_neighbours[current]:
                if graph_costs[neighbour] == BFS.NOT_VISITED:
                    graph_costs[neighbour] = cost
                    queue.append(neighbour)

        return graph_costs

    # ########################################################################
    # ###################################################### PRINT DEBUG_ ####
    # TODO: REMOVE ??
    def print_debug(self, graph_costs: dict[Vec2, int]) -> None:
        """Print the maze according to the current values."""

        def colour(value: int):
            if value == 0:
                return "white"
            if value > 45:
                value -= 45
                red = (100 + value * 2) % 255
                green = 150
                blue = (80 + value * 2) % 255
            else:
                red = (255 - value * 5) % 255
                green = (50 + value * 2) % 255
                blue = (0 + value * 3) % 255

            return (red, green, blue)

        if graph_costs:
            size = VData.SPRITE_SIZE

            # --
            x_max = max(self.graph_neighbours.keys(), key=lambda k: k.x)
            y_max = max(self.graph_neighbours.keys(), key=lambda k: k.y)

            for y in range(int(y_max.y) + size, -size, -size):
                for x in range(0, int(x_max.x) + size * 2, size):
                    point = Vec2(x, y)

                    if point in graph_costs:
                        if graph_costs[point] == BFS.NOT_VISITED:
                            cprint(" . ", end="", color="grey")
                        else:
                            # colour = "red" if point in self.path else "yellow"
                            cprint(
                                f"{graph_costs[point] % 100:>3}",
                                end="",
                                color=colour(graph_costs[point]),
                            )

                    elif point in self.graph_neighbours.keys():
                        print("   ", end="")
                    else:
                        cprint("███", end="", color="light_grey")

                print()
