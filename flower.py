import arcade
import random

class Flower(arcade.Sprite):
    def __init__(self):
        super().__init__()

    @classmethod
    def setup(cls, flowers_list, bottom_obstacles_list, top_obstacles_list):
        number_of_flowers = random.randrange(1, 3)
        for i in range(number_of_flowers):
            # make sure flowers are not being placed on top of obstacles

        return flowers_list
