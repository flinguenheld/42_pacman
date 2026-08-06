import random
from arcade import Vec2


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░▀█▀░█▀▄░█▀█░█░░░▀█▀░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░░█░░█▀▄░█░█░█░░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░▀░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class Patroling:
    """
    Patroling algorithm,
    From the maze graph {floor point: list of all neighbours} and a start:
      - Randomly get a next position.
      - Remember the path to avoid come back.
    """

    def __init__(self, graph_neighbours: dict[Vec2, list[Vec2]]):
        self.graph_neighbours = graph_neighbours
        self.forbidden: set[Vec2] = set()

    # ########################################################################
    # ############################################## NEXT RANDOM POSITION ####
    def next_random_positon(self, start: Vec2) -> Vec2:
        # TODO: Add a way to keep the enemy close to its corner ?
        # TODO: A kind of probabilty to select a closer point
        # TODO: when it's far away...

        neighbours = self.graph_neighbours[start]
        neighbours = [n for n in neighbours if n not in self.forbidden]

        if not neighbours:
            self.forbidden.clear()
            return self.next_random_positon(start)

        choice = random.choice(neighbours)
        self.forbidden.add(choice)
        return choice
