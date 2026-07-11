from arcade.hitbox import HitBox
from arcade import Vec2, TextureAnimationSprite, TextureAnimation


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░░
class VEntitySprite(TextureAnimationSprite):
    HITBOX_SCALE = 0.5

    def __init__(
        self,
        animation: TextureAnimation,
        center: Vec2,
        scale: float,
    ) -> None:
        super().__init__(
            animation=animation,
            center_x=center.x,
            center_y=center.y,
            scale=scale,
        )

        self.hit_box = self.generate_hit_box()

    # ########################################################################
    # ################################################## GENERATE HIT BOX ####
    def generate_hit_box(self) -> HitBox:

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
            scale=Vec2(VEntitySprite.HITBOX_SCALE, VEntitySprite.HITBOX_SCALE),
        )
