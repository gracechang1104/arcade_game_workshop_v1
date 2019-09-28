import arcade
import random
import os

obstacle = "sprites/wall.png"

class Obstacle(arcade.Sprite):

    def __init__(self):
        super().__init__()

    @classmethod
    def setup_obstacles(cls, bottom_list, top_list):
        # place obstacle sprites by having the same 'x' and gape throughout, but gapes btwn top & bottom pipes are
        # different ie randomized gap instead of placement
        prev_wall_x = 0
        max_centre_y = 60
        min_centre_y = 0
        min_gap = 50

        for i in range(4):
            cls.bottom_obstacle = arcade.Sprite("sprites/obstacle.png", 1)
            if prev_wall_x == 0:
                cls.bottom_obstacle.center_x = 100
                prev_wall_x = cls.bottom_obstacle.center_x
            else:
                cls.bottom_obstacle.center_x = prev_wall_x + 300
                prev_wall_x = cls.bottom_obstacle.center_x
            cls.bottom_obstacle.center_y = random.randrange(min_centre_y, max_centre_y)
            bottom_wall_y = cls.bottom_obstacle.center_y
            bottom_list.append(cls.bottom_obstacle)

            cls.top_obstacle = arcade.Sprite("sprites/obstacle.png", 1)
            cls.top_obstacle.angle = 180
            cls.top_obstacle.center_x = prev_wall_x
            cls.top_obstacle.center_y = 500 - bottom_wall_y + min_gap
            top_list.append(cls .top_obstacle)

        return bottom_list, top_list

    def kill_obstacles(obstacles_list):
        while len(obstacles_list) != 0:
            for obstacle in obstacles_list:
                obstacle.kill()





