import arcade

SPRITE_STARTING_X = 0
SPRITE_STARTING_Y = 500/2

# Constants to scale sprites
CHARACTER_SCALE_HALF = 0.5

class Bee(arcade.Sprite):
    def __init__(self):
        super().__init__()

    @classmethod
    def setup_bee(cls):
        # initiate & place bee sprite
        bee_sprite = arcade.Sprite("sprites/bumblebee_sprite.png", CHARACTER_SCALE_HALF)
        bee_sprite.center_x = SPRITE_STARTING_X
        bee_sprite.center_y = SPRITE_STARTING_Y

        return bee_sprite
