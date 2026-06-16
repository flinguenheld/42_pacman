import arcade


class VMain(arcade.Window):
    def __init__(self):
        super().__init__(400, 400, "Hello")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Draw everything"""
        self.clear()
