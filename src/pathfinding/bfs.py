import sys
from collections import deque

from arcade import Vec2


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
    def get_costs(self, start: Vec2) -> dict[Vec2, int]:
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
