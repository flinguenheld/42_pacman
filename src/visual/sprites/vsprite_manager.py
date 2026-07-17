from arcade.types import Color

from src.visual.vdata import VStyles
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor
from src.visual.gui.gbackground import GBackground


# ░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░


# QUESTION: RENAME IT ? Since some sprites are also manage in VEntity...
# QUESTION: RENAME IT ? Since some sprites are also manage in VEntity...
class SpriteManager:
    def __init__(self, atlas: VAtlas, maze: Maze) -> None:
        self.style: VStyles = VStyles.EDGE

        self.atlas = atlas
        self.maze = maze
        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas)
        self.background: GBackground = GBackground(self.atlas)

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, maze: Maze, reload_atlas: bool = False) -> None:
        if reload_atlas:
            self.atlas.load()

        self.walls.reload(maze.walls.union(maze.forty_two), maze.floors)
        self.floors.reload(maze.floors)
        self.background.build(self.maze.center_position, self.maze.rect)

    # ########################################################################
    # ############################################################ UPDATE ####
    def update(self, delta_time: int | float) -> None:
        self.background.update(delta_time)
        self.walls.update_animation(delta_time)
        self.floors.update_animation(delta_time)

    # ########################################################################
    # ############################################################## DRAW ####
    def draw(self) -> None:
        self.background.draw()
        self.walls.sprites.draw(pixelated=True)
        self.floors.sprites.draw(pixelated=True)

    # ########################################################################
    # ################################################## BACKGROUND COLOR ####
    @property
    def background_color(self) -> Color:
        return self.atlas.get_color("background")
