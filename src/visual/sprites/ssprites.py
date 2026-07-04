import arcade
import random
from arcade import Sprite, SpriteList, Vec2

from src.visual import VData
from src.maze.maze_wrapper import Maze
from src.visual.vatlas import VAtlas, VTile


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░
class SSprites:
    def __init__(self, atlas: VAtlas, base_name: str) -> None:
        self.sprites: SpriteList[Sprite] = SpriteList(use_spatial_hash=True)
        self.base_name: str = base_name
        self.atlas = atlas

        self._clear_edges()

    # ########################################################################
    # ######################################################## ADD SPRITE ####
    def add_sprite(
        self,
        texture_name: str,
        center: Vec2,
        force_first_texture: bool = False,
        sprite_size: int = VData.SPRITE_SIZE,
    ) -> None:
        # ############################### PICK TEXTURE ####
        def pick_texture(who: str) -> VTile:
            if force_first_texture:
                return self.atlas.textures[who][0]

            tile = [t for t in self.atlas.textures[who]]
            weights = [w.probability / 100 for w in self.atlas.textures[who]]

            return random.choices(tile, weights, k=1)[0]

        # ####################################
        tile = pick_texture(texture_name)
        angle = random.choice(tile.allowed_angles)
        # center = Maze.to_world_coords(center)
        self._up_edges(center)

        if isinstance(tile.texture, arcade.TextureAnimation):
            sprite_animation: Sprite = arcade.TextureAnimationSprite(
                animation=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=self._get_scale(tile.width, sprite_size),
            )
            sprite_animation.angle = angle
            self.sprites.append(sprite_animation)
        else:
            self.sprites.append(
                arcade.Sprite(
                    path_or_texture=tile.texture,
                    center_x=center.x,
                    center_y=center.y,
                    scale=self._get_scale(tile.width, sprite_size),
                    angle=angle,
                )
            )

    # ########################################################################
    # ############################################################# SCALE ####
    def _get_scale(self, size: int, sprite_size: int) -> float:
        return sprite_size / size

    # ########################################################################
    # ############################################################# CLEAR ####
    def clear(self) -> None:
        self.sprites.clear()
        self._clear_edges()

    # ########################################################################
    # ############################################################# EDGES ####
    def _clear_edges(self):
        self._top = 0.0
        self._bot = 0.0
        self._left = 0.0
        self._right = 0.0

    def _up_edges(self, point: Vec2):
        """
        Save the edges.
        Used while adding new sprites to avoid calculations.
        """
        if point.y < self._bot:
            self._bot = point.y
        if point.y > self._top:
            self._top = point.y

        if point.x < self._left:
            self._left = point.x
        if point.x > self._right:
            self._right = point.x

    # ########################################################################
    # ######################################################## PROPERTIES ####
    @property
    def center_position(self):
        center = Vec2(self._left + self.width / 2, self._bot + self.height / 2)
        return center

    @property
    def width(self):
        return self._right - self._left

    @property
    def height(self):
        return self._top - self._bot

    # ########################################################################
    # ################################################## UPDATE ANIMATION ####
    def update_animation(self, delta_time: int | float) -> None:
        self.sprites.update_animation(delta_time)
