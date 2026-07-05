import arcade
from typing import Any
from json import load as json_load
from src.visual import Style, VData
from dataclasses import dataclass, field
from arcade import TextureAnimation, Texture


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
        self.style = Style.SUMMER
        self.info: dict[str, Any] = dict()
        self.textures: dict[str, list[VTile]] = dict()

    # ########################################################################
    # ############################################################## LOAD ####
    def load(self, new_style: Style) -> None:
        self.style = new_style
        self._load_info()
        self._load_textures()

    # ########################################################################
    # ############################################# LOAD INFORMATION FILE ####
    def _load_info(self) -> None:
        self.path = f"{VData.TEXTURES}/{self.style.value}"
        self.info = self._open_info_file(self.path)
        self.default_width = self.info["default_width"]
        self.default_height = self.info["default_height"]

    # ########################################################################
    # ##################################################### LOAD TEXTURES ####
    def _load_textures(self) -> None:
        width = -1
        height = -1
        self.textures.clear()
        sheet = arcade.load_spritesheet(f"{self.path}/sheet.png")

        # #################################### REGULAR #######
        def add_regular(y: int, data_line: dict[str, Any]) -> None:

            for x in range(data_line["nb"]):
                x *= width
                texture = sheet.get_texture(arcade.LBWH(x, y, width, height))
                self.textures[data_line["name"]].append(
                    VTile(
                        texture,
                        width,
                        height,
                        self._get_data(data_line, "probability", 100),
                        self._get_data(data_line, "allowed_rotation", [0]),
                    )
                )

        # ################################### ANIMATED #######
        def add_animation(y: int, data: dict[str, Any]) -> None:
            keyframes = []

            duration = -1
            for x in range(data["nb"]):
                if x < len(data["duration"]):
                    duration = data["duration"][x]

                x *= width
                texture = sheet.get_texture(arcade.LBWH(x, y, width, height))
                keyframes.append(arcade.TextureKeyframe(texture, duration))

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

            if data_line["name"] not in self.textures:
                self.textures[data_line["name"]] = list()

            if self._get_data(data_line, "animated", False):
                add_animation(y, data_line)
            else:
                add_regular(y, data_line)

            y += height

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
    # ################################################## BACKGROUND COLOR ####
    @property
    def background_color(self) -> dict[str, int] | Any:
        return self.info["background_color"]
