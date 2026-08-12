import random

from arcade import Vec2

from src.maze.maze import Maze
from src.utils.utils import print_debug


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░▀█▀░█▀▄░█▀█░█░░░█░░░▀█▀░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░░█░░█▀▄░█░█░█░░░█░░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░▀░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class Patrolling:
    """
    Patrolling algorithm,
    From the maze graph {floor point: list of all neighbours} and a start:
      - Randomly get a next position.
      - Remember the path to avoid coming back.
      - Manage a home mode:

          + Set a trigger (the distance from corner to the maze center).
          + If the given start is further than the home trigger:
              - Set patrolling as 'home mode'.
              - 'Next position' will return the shortest path to the corner.
              - Once reached, unset 'home mode'
    """

    def __init__(self, maze: Maze, corner_id: int):
        self.maze = maze
        self.corner_id = corner_id
        self.forbidden: set[Vec2] = set()

        # Home mode --
        self.home_state = False
        self.home_to_reach = 0
        self.home_trigger = self.maze.graph_corners[self.corner_id][
            self.maze.floor_center
        ]
        self.print_debug(f"Home trigger init: {self.home_trigger} !")

    # ########################################################################
    # ##################################################### NEXT POSITION ####
    def next_position(self, start: Vec2) -> Vec2:
        """Return a random next point or the next point to the corner."""

        self._home_mode_manager(start)

        if self.home_state:
            return self.maze.get_next_lowest(start, corner=self.corner_id)
        else:
            return self._next_random_position(start)

    # ########################################################################
    # ############################################## CORNER ####
    def _home_mode_manager(self, start: Vec2) -> None:
        """
        Set/unset the home mode according to the given start.
        """

        dist_to_corner = self.maze.graph_corners[self.corner_id][start]
        if self.home_state:
            if dist_to_corner <= self.home_to_reach:
                self.print_debug("Corner reached")
                self.home_state = False

        elif dist_to_corner > self.home_trigger:
            self.home_state = True
            self.home_to_reach = random.randint(2, self.home_trigger // 2)
            self.print_debug(f"Go back to corner up to {self.home_to_reach}")

    # ########################################################################
    # ############################################## NEXT RANDOM POSITION ####
    def _next_random_position(self, start: Vec2) -> Vec2:
        """Get a next random point."""

        neighbours = self.maze.graph_neighbours[start]
        neighbours = [n for n in neighbours if n not in self.forbidden]

        if not neighbours:
            # self.print_debug("No neighbour anymore!")
            self.forbidden.clear()
            return self._next_random_position(start)

        choice = random.choice(neighbours)
        self.forbidden.add(choice)
        return choice

    # ########################################################################
    # ####################################################### PRINT DEBUG ####
    def print_debug(self, text: str) -> None:
        print_debug(f"Patrolling {self.corner_id}: {text}")
