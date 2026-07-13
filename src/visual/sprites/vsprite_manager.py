from arcade.types import Color

from src.visual.vdata import VStyles
from src.visual.vatlas import VAtlas
from src.maze.maze_wrapper import Maze
from src.visual.sprites.swall import SWall
from src.visual.sprites.sfloor import SFloor
from src.visual.sprites.sbackground import SBackground


# ░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░


# QUESTION: RENAME IT ? Since some sprites are also manage in VEntity...
# QUESTION: RENAME IT ? Since some sprites are also manage in VEntity...
class SpriteManager:
    def __init__(self) -> None:
        self.style: VStyles = VStyles.EDGE
        # TODO: MOVE THE ATLAS IN VGAME
        # TODO: MOVE THE ATLAS IN VGAME
        self.atlas = VAtlas()
        self.atlas.load(self.style)

        self.walls: SWall = SWall(self.atlas)
        self.floors: SFloor = SFloor(self.atlas)
        self.backgrounds: SBackground = SBackground(self.atlas)

    # ########################################################################
    # ######################################################## NEXT STYLE ####
    # TODO: MOVE NEXT STYLE IN VGAME
    # TODO: MOVE NEXT STYLE IN VGAME
    def next_style(self) -> None:
        match self.style:
            case VStyles.SUMMER:
                self.style = VStyles.EDGE

            case VStyles.EDGE:
                self.style = VStyles.SUMMER

    # ########################################################################
    # ############################################################ RELOAD ####
    def reload(self, maze: Maze, reload_atlas: bool = False) -> None:
        if reload_atlas:
            self.atlas.load(self.style)

        self.walls.reload(maze.walls.union(maze.forty_two), maze.floors)
        self.floors.reload(maze.floors)
        self.backgrounds.reload(maze.background, maze)

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

    # ########################################################################
    # ################################################## BACKGROUND COLOR ####
    @property
    def background_color(self) -> Color:
        return Color(**self.atlas.background_color)
