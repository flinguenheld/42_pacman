from arcade.hitbox import HitBox
import arcade
from src.visual.vatlas import VAtlas, VTile
from abc import ABC

from arcade import Vec2, TextureAnimationSprite


class VEntity(ABC):
    def __init__(self, atlas: VAtlas, sprite_name: str, position: Vec2):
        self._atlas: VAtlas = atlas
        self._sprite_name = sprite_name
        self._current_direction = "wait"

        self.set_sprite()
        self.position = position

        self.setup()

    def setup(self) -> None:
        pass

    @property
    def position(self) -> Vec2:
        return Vec2(self.sprite.center_x, self.sprite.center_y)

    @position.setter
    def position(self, where: Vec2) -> None:
        self.sprite.center_x = where.x
        self.sprite.center_y = where.y

    def update(self, delta_time: float = 1 / 60) -> None:
        pass

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.sprite.update_animation(delta_time)

    def set_sprite(self, where: str = "left") -> None:

        if self._current_direction != where:
            # print(f"find this one: {self._sprite_name}_{where}")
            tile = self._atlas.textures[f"{self._sprite_name}_{where}"][0]

            # TODO: ADD A SCALE METHOD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if isinstance(tile.texture, arcade.TextureAnimation):
                self.sprite = VSpriteEntity(
                    animation=tile.texture, center=Vec2(100, 100)
                )

                self._current_direction = where

        # if sprite is None:
        #     self.sprite = None
        #     return
        # else:
        #     sprite.position = self.position
        #     self.sprite = sprite

    def on_up_movement(self) -> None:
        pass

    def on_down_movement(self) -> None:
        pass

    def on_left_movement(self) -> None:
        pass

    def on_right_movement(self) -> None:
        pass

    # def set_sprite(self, name:str):
    #     self.sprite = VPlayerSprite()


class VEntityMovement(VEntity):
    def __init__(self, atlas: VAtlas, sprite_name: str, position: Vec2):
        super().__init__(atlas, sprite_name, position)
        self._change_x = 0.0
        self._change_y = 0.0

    @property
    def change_x(self) -> float:
        return self._change_x

    @change_x.setter
    def change_x(self, value: float) -> None:

        # if value != 0:

        # if self.sprite:
        self.sprite.change_x = value
        self._change_x = value

        if value > 0:
            self.set_sprite("right")
        elif value < 0:
            self.set_sprite("left")

    @property
    def change_y(self) -> float:
        return self._change_y

    @change_y.setter
    def change_y(self, value: float) -> None:

        # if value != 0:

        # if self.sprite:
        self.sprite.change_y = value
        self._change_y = value

        # TODO ADD ==0 TO WAIT
        # TODO PREVENT MOVE BOTH ON X AND Y
        # TODO PREVENT MOVE BOTH ON X AND Y
        # TODO PREVENT MOVE BOTH ON X AND Y
        # TODO PREVENT MOVE BOTH ON X AND Y
        if value > 0:
            self.set_sprite("top")
        elif value < 0:
            self.set_sprite("bot")


class VSpriteEntity(TextureAnimationSprite):
    def __init__(self, animation, center) -> None:
        # super().__init__(VData.TEXTURES + "/hen.png", scale=0.3)
        super().__init__(
            animation=animation,
            center_x=center.x,
            center_y=center.y,
            scale=1,
        )

        self.hitbox_scale: float = 0.50
        self.hit_box = self.generate_hit_box()

    def generate_hit_box(self) -> HitBox:
        scale = self.hitbox_scale

        half_w: float = self.width / 2
        half_h: float = self.height / 2
        return HitBox(
            points=[
                (-half_w, -half_h),
                (half_w, -half_h),
                (half_w, half_h),
                (-half_w, half_h),
            ],
            position=self.position,
            scale=Vec2(scale, scale),
        )
