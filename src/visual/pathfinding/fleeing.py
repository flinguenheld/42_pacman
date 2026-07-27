import random
from arcade import Vec2


class Fleeing:
    """
    Very very basic fleeing algo, to up.
    """

    def __init__(self, graph: dict[Vec2, list[Vec2]]):
        self.graph = graph

    # ########################################################################
    # ############################################################### RUN ####
    def run_algo(self, start: Vec2, target: Vec2) -> Vec2:

        possibles = [v for v in self.graph[start] if v != target]

        if not possibles:
            return start

        return random.choice(possibles)
