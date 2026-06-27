import arcade
from typing import Any
from dataclasses import dataclass
from json import load as json_load
from src.visual import StyleRENAME, VData
from arcade import TextureAnimation, Texture


@dataclass
class VTile:
    texture: Texture | TextureAnimation
    no_rotation: bool = False
    probability: int = 100


class VAtlas:
    def __init__(self):
        self.style = StyleRENAME.Pirate
        self.info: dict[str, Any] = dict()
        self.textures: dict[str, list[VTile]] = dict()

    @property
    def size(self) -> int:
        return self.info["size"]

    # ########################################################################
    # ######################################################## NEXT STYLE ####
    def next_style(self) -> None:
        self.style: StyleRENAME = StyleRENAME.Pirate

    # ########################################################################
    # #################################################### LOAD INFO FILE ####
    def load_info(self) -> None:

        self.path = f"{VData.TEXTURES}/{self.style.value}"
        self.info = self._open_info_file(self.path)
        print(self.info)

    def get_option(
        self, data: dict[str, Any], option: str, default: Any
    ) -> Any:

        if option in data:
            return data[option]
        return default

    # ########################################################################
    # ##################################################### LOAD TEXTURES ####
    def load_textures(self):
        self.textures.clear()
        size = self.info["size"]
        sheet = arcade.load_spritesheet(f"{self.path}/sheet.png")

        def add_regular(y: int, data_line: dict[str, Any]) -> None:

            for x in range(data_line["nb"]):
                x *= size
                texture = sheet.get_texture(arcade.LBWH(x, y, size, size))
                self.textures[data_line["name"]].append(
                    VTile(
                        texture,
                        self.get_option(data_line, "no_rotation", False),
                        self.get_option(data_line, "probability", 100),
                    )
                )

        def add_animation(y: int, data: dict[str, Any]) -> None:
            keyframes = []

            for x in range(data["nb"]):
                x *= size
                texture = sheet.get_texture(arcade.LBWH(x, y, size, size))

                if x == 0:
                    duration = data["duration_first"]
                else:
                    duration = data["duration"]

                keyframes.append(arcade.TextureKeyframe(texture, duration))

            animation = arcade.TextureAnimation(keyframes=keyframes)
            self.textures[data_line["name"]].append(
                VTile(
                    animation,
                    self.get_option(data_line, "no_rotation", False),
                    self.get_option(data_line, "probability", 100),
                )
            )

        # ###################################################
        # #####################################################
        for y, data_line in enumerate(self.info["lines"]):
            y *= self.info["size"]

            if data_line["name"] not in self.textures:
                self.textures[data_line["name"]] = list()

            if self.get_option(data_line, "animated", False):
                add_animation(y, data_line)
            else:
                add_regular(y, data_line)

    # ########################################################################
    # ####################################################### SPRITE INFO ####
    def _open_info_file(self, path: str) -> dict[str, Any]:
        try:
            with open(f"{path}/info.json", "r") as file:
                info: dict[str, Any] = json_load(file)
                return info
        except OSError:
            raise FileNotFoundError(f"info.json not found in {path}")
