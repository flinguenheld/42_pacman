import random
import arcade
from arcade.types import Color
from typing import Any, Sequence
from json import load as json_load
from dataclasses import dataclass, field
from arcade import (
    TextureAnimationSprite,
    TextureAnimation,
    Texture,
    Sprite,
    Vec2,
)
from src.visual.vdata import VStyles, VData


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░░█░░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░░
@dataclass
class VTile:
    texture: Texture | TextureAnimation
    width: int
    height: int
    probability: int = 100
    allowed_angles: list[int] = field(default_factory=lambda: [0])


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▀█▀░█░░░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀█░░█░░█░░░█▀█░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░░
class VAtlas:
    INFO_FILENAME = "info.json"

    def __init__(self) -> None:
        self.style = VStyles.EDGE
        self.info: dict[str, Any] = dict()
        self.textures: dict[str, list[VTile]] = dict()

    # ########################################################################
    # ############################################################## LOAD ####
    def load(self) -> None:
        self._load_info()
        self._load_textures()

    # ########################################################################
    # ######################################################## NEXT STYLE ####
    # TODO: MOVE NEXT STYLE IN VGAME OR WHERE ????
    # TODO: MOVE NEXT STYLE IN VGAME OR WHERE ????
    def next_style(self) -> None:
        match self.style:
            case VStyles.EDGE:
                self.style = VStyles.EDGE_NO_TILE

            case VStyles.EDGE_NO_TILE:
                self.style = VStyles.EDGE_RED

            case VStyles.EDGE_RED:
                self.style = VStyles.EDGE

        self.load()

    # ########################################################################
    # ############################################# LOAD INFORMATION FILE ####
    def _load_info(self) -> None:
        self.path = f"{VData.TEXTURES}/{self.style.value}"
        self.info = self._open_info_file(self.path)
        self.default_width = self.info["default_width"]
        self.default_height = self.info["default_height"]
        self.default_hitbox = self.info["default_hitbox"]

    # ########################################################################
    # ##################################################### LOAD TEXTURES ####
    def _load_textures(self) -> None:
        width = -1
        height = -1
        self.textures.clear()
        sheet = arcade.load_spritesheet(f"{self.path}/sheet.png")

        # ############################# CREATE TEXTURE #######
        def create_texture_with_hitbox(x: int, y: int) -> Texture:
            """
            Extract the image at the given coordinates to create a texture.
            Apply the hitbox calculated for the line.
            If hitbox is None, arcade automatically uses the simple algorithm.
            """

            image = sheet.get_image(arcade.LBWH(x, y, width, height))
            return Texture(image=image, hit_box_points=hitbox)

        # #################################### REGULAR #######
        def add_regular_texture(y: int, data_line: dict[str, Any]) -> None:

            for x in range(data_line["nb"]):
                x *= width

                self.textures[data_line["name"]].append(
                    VTile(
                        create_texture_with_hitbox(x, y),
                        width,
                        height,
                        self._get_data(data_line, "probability", 100),
                        self._get_data(data_line, "allowed_rotation", [0]),
                    )
                )

        # ################################### ANIMATED #######
        def add_animated_texture(y: int, data: dict[str, Any]) -> None:
            keyframes = []

            duration = -1
            for x in range(data["nb"]):
                if x < len(data["duration"]):
                    duration = data["duration"][x]

                x *= width
                keyframes.append(
                    arcade.TextureKeyframe(
                        create_texture_with_hitbox(x, y),
                        duration,
                    )
                )

            animation = arcade.TextureAnimation(keyframes=keyframes)
            self.textures[data_line["name"]].append(
                VTile(
                    animation,
                    width,
                    height,
                    self._get_data(data_line, "probability", 100),
                    self._get_data(data_line, "allowed_rotation", [0]),
                )
            )

        # #################################################
        # ####################################################
        y = 0
        for data_line in self.info["lines"]:
            width = self._get_data(data_line, "width", self.default_width)
            height = self._get_data(data_line, "height", self.default_height)

            # Only One hitbox for the line even if it's an animation
            hitbox = self._generate_hitbox(data_line, height, width)

            # Allows the atlas to have several textures with the same name
            if data_line["name"] not in self.textures:
                self.textures[data_line["name"]] = list()

            if self._get_data(data_line, "animated", False):
                add_animated_texture(y, data_line)
            else:
                add_regular_texture(y, data_line)

            y += height

    # ########################################################################
    # ################################################### GENERATE HITBOX ####
    def _generate_hitbox(
        self,
        data_line: dict[str, Any],
        height: int,
        width: int,
    ) -> Sequence | None:
        """
        Fill the hitbox line field with the defaults.
        Create the hitbox according to values.
        Return None if the hitbox has to be calculated by arcade.
        """

        # Fill with no given values --
        hitbox = self._get_data(data_line, "hitbox", self.default_hitbox)
        for key, val in self.default_hitbox.items():
            if key not in hitbox:
                hitbox[key] = val

        if hitbox["automatic"]:  # None will result in an automatic hitbox
            return None

        if hitbox["deactivated"]:
            return ((0, 0), (0, 0))

        # --
        size = hitbox["size"]
        top: float = height / 2 if hitbox["full_top"] else size / 2
        right: float = width / 2 if hitbox["full_right"] else size / 2
        bot: float = -height / 2 if hitbox["full_bot"] else -size / 2
        left: float = -width / 2 if hitbox["full_left"] else -size / 2

        if hitbox["bevel"] <= 0 or hitbox["bevel"] * 2 > size:
            return (
                (left, bot),
                (left, top),
                (right, top),
                (right, bot),
            )
        else:
            return (
                (left + hitbox["bevel"], bot),
                (left, bot + hitbox["bevel"]),
                (left, top - hitbox["bevel"]),
                (left + hitbox["bevel"], top),
                (right - hitbox["bevel"], top),
                (right, top - hitbox["bevel"]),
                (right, bot + hitbox["bevel"]),
                (right - hitbox["bevel"], bot),
            )

    # ########################################################################
    # ######################################################## GET OPTION ####
    def _get_data(
        self,
        data: dict[str, Any],
        option: str,
        default: Any,
    ) -> Any:

        if option in data:
            return data[option]
        return default

    # ########################################################################
    # #################################################### OPEN JSON FILE ####
    def _open_info_file(self, path: str) -> dict[str, Any]:
        try:
            with open(f"{path}/{VAtlas.INFO_FILENAME}", "r") as file:
                info: dict[str, Any] = json_load(file)
                return info
        except OSError:
            raise FileNotFoundError(f"info.json not found in {path}")

    # ########################################################################
    # ############################################################ COLORS ####
    def get_color(self, name: str) -> Color:

        if name not in self.info["colors"]:
            assert KeyError(f"Color '{name}' does not exist in the info.json.")

        return Color(**self.info["colors"][name])

    # ########################################################################
    # ############################################################## FONT ####
    @property
    def font_name(self) -> str:
        return str(self.info["font"]["name"])

    @property
    def font_size(self) -> int:
        return int(self.info["font"]["size"])

    # ########################################################################
    # ###################################### NUMBER OF ENEMIES IN THE PNG ####
    @property
    def nb_of_enemies(self) -> int:
        return int(self.info["number_of_enemies"])

    # ########################################################################
    # ######################################################### PICK TILE ####
    def pick_tile(self, name: str, randomly: bool = True) -> VTile:
        """
        Get one of the tile with the given name.
        Respect the given probabilites in the info.json file.
        """

        if not randomly:
            return self.textures[name][0]

        tile = [t for t in self.textures[name]]
        weights = [w.probability / 100 for w in self.textures[name]]

        return random.choices(tile, weights, k=1)[0]

    # ########################################################################
    # #################################################### TILE TO SPRITE ####
    def tile_to_sprite(
        self,
        tile: VTile,
        center: Vec2,
        angle: int = 0,
        sprite_size: int = VData.SPRITE_SIZE,
    ) -> Sprite | TextureAnimationSprite:
        """
        Create a Sprite from the given VTile.
        """

        if isinstance(tile.texture, arcade.TextureAnimation):
            sprite_animated = arcade.TextureAnimationSprite(
                animation=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=sprite_size / tile.width,
            )
            sprite_animated.angle = angle
            return sprite_animated
        else:
            return arcade.Sprite(
                path_or_texture=tile.texture,
                center_x=center.x,
                center_y=center.y,
                scale=sprite_size / tile.width,
                angle=angle,
            )
