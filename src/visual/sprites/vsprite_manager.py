import time
import random
from src.visual import Style
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor
from src.visual.sprites.sbackground import SBackground


# ░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░
class SpriteManager:
    def __init__(self) -> None:
        self.atlas = VAtlas()
        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas)
        self.backgrounds: SBackground = SBackground(self.atlas)
        self.style: Style = Style.SUMMER

    # ########################################################################
    # ######################################################## NEXT STYLE ####
    def next_style(self) -> None:
        match self.style:
            case Style.SUMMER:
                self.style = Style.SUMMER
            # case Style.PIRATE:
            #     self.style = Style.PIRATE_GREEN
            # case Style.PIRATE_GREEN:
            #     self.style = Style.PIRATE

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, maze: Maze) -> None:
        random.seed(time.time())
        self.atlas.load(self.style)
        self.walls.reload(maze.walls.union(maze.forty_two), maze.floors)
        self.floors.reload(maze.floors)
        self.backgrounds.reload(maze.background)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.walls.update_animation(delta_time)
        self.floors.update_animation(delta_time)
        self.backgrounds.update_animation(delta_time)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.backgrounds.sprites.draw(pixelated=True)
        self.walls.sprites.draw(pixelated=True)
        self.floors.sprites.draw(pixelated=True)
