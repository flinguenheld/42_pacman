from mazegenerator import MazeGenerator


# ░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░░█▀▀░█▀▀░█▀█░░░█░█░█▀▄░█▀█░█▀█░█▀█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░░█░█░█▀▀░█░█░░░█▄█░█▀▄░█▀█░█▀▀░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░░░▀░░░▀▀▀░▀░▀░░
class MazeGeneratorWrapper:
    """
    Generator wrapper.
    Allow you to generate a new maze from the generator.
    The generated maze is an array of hexadecimal values.
    Then convert it in an array of int to be used by the Maze class.
        - 0 -> floor
        - 1 -> wall
    """

    def __init__(self) -> None:
        self.setup()

    # ########################################################################
    # ############################################################# SETUP ####
    def setup(self) -> None:
        self.hexa_maze: list[list[int]] = list()
        self.raw_maze: list[list[int]] = list()

    # ########################################################################
    # ################################################# GENERATE NEW MAZE ####
    def generate_new_maze(
        self,
        raw_width: int = 15,
        raw_height: int = 15,
        seed: int = 42,
    ) -> None:

        try:
            maze_gen = MazeGenerator(
                size=(raw_width, raw_height),
                perfect=False,
                seed=seed,
            )
            self.setup()
            self.hexa_maze = maze_gen.maze
            self._hexa_to_raw()

        except RecursionError:
            # TODO: add something ????
            exit(42)

    def _hexa_to_raw(self) -> None:
        """
        Loop in the raw maze to fill maze
        !! Arcade works from bottom left with X, Y !!
        !! Reverse the logic !!
        !! Reverse on Y !!

        hexa ->       0       1       2       3       4
         |
         v   raw  0   1   2   3   4   5   6   7   8   9  10

                ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
             0  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         0   1  ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             2  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         1   3  ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             4  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         2   5  ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃ O ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             6  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
        """

        # 0 -> floor
        # 1 -> wall

        self.raw_maze = [
            [0 for _ in range(len(self.hexa_maze[0]) * 2 + 1)]
            for _ in range(len(self.hexa_maze) * 2 + 1)
        ]

        for hexa_y, row in enumerate(reversed(self.hexa_maze)):
            for hexa_x, value in enumerate(row):
                # Get world coordinates --
                y = hexa_y * 2 + 1
                x = hexa_x * 2 + 1

                # --
                if value & 0b0001 == 0b0001:  # Top
                    self.raw_maze[y + 1][x] = 1
                    self.raw_maze[y + 1][x - 1] = 1
                    self.raw_maze[y + 1][x + 1] = 1

                if value & 0b0100 == 0b0100:  # Bottom
                    self.raw_maze[y - 1][x] = 1
                    self.raw_maze[y - 1][x - 1] = 1
                    self.raw_maze[y - 1][x + 1] = 1

                if value & 0b1000 == 0b1000:  # Left
                    self.raw_maze[y][x - 1] = 1
                    self.raw_maze[y - 1][x - 1] = 1
                    self.raw_maze[y + 1][x - 1] = 1

                if value & 0b0010 == 0b0010:  # Right
                    self.raw_maze[y][x + 1] = 1
                    self.raw_maze[y - 1][x + 1] = 1
                    self.raw_maze[y + 1][x + 1] = 1

                if value & 0b1111 == 0b1111:  # 42
                    self.raw_maze[y][x] = 1
