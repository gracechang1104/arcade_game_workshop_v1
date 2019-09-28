import arcade
import random

class Flower(arcade.Sprite):
    def __init__(self):
        super().__init__()

    @classmethod
    def setup(cls, flowers_list, bottom_obstacles_list, top_obstacles_list):
        number_of_flowers = random.randrange(1, 3)
        for i in range(number_of_flowers):
            flower = arcade.Sprite("sprites/flower_sprite.png", 0.5)

            # make sure flowers are not being placed on top of obstacles

            flower_placed = False

            while not flower_placed:
                flower.center_x = random.randrange(100, 900)
                flower.center_y = random.randrange(300, 400)

                collision_with_top_obstacle = arcade.check_for_collision_with_list(flower, top_obstacles_list)
                collision_with_bottom_obstacle = arcade.check_for_collision_with_list(flower,
                                                                                      bottom_obstacles_list)

                if len(collision_with_top_obstacle) == 0 and len(collision_with_bottom_obstacle) == 0:
                    flower_placed = True
                    flowers_list.append(flower)

        return flowers_list