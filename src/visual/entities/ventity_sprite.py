from arcade.hitbox import HitBox
from arcade import Vec2, TextureAnimationSprite, TextureAnimation


# ░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░░░█▀▀░█▀█░█▀▄░▀█▀░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░█▀▀░█░█░░█░░░█░░░█░░░█░░░░▀▀█░█▀▀░█▀▄░░█░░░█░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░▀░░░▀░░░░▀▀▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░░
class VSpriteEntity(TextureAnimationSprite):
    def __init__(self, animation: TextureAnimation, center: Vec2) -> None:
        # TODO: DEAL WITH THE SCALE ---------------------------------
        # TODO: DEAL WITH THE SCALE ---------------------------------
        # TODO: DEAL WITH THE SCALE ---------------------------------
        super().__init__(
            animation=animation,
            center_x=center.x,
            center_y=center.y,
            scale=1,
        )

        # TODO: DEAL WITH THIS MAGIC NUMBER ---------------------------------
        # TODO: DEAL WITH THIS MAGIC NUMBER ---------------------------------
        # TODO: DEAL WITH THIS MAGIC NUMBER ---------------------------------
        self.hitbox_scale: float = 0.50
        self.hit_box = self.generate_hit_box()

    # ########################################################################
    # ################################################## GENERATE HIT BOX ####
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
