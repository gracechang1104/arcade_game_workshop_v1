import arcade
import bee
from bee import Bee
from obstacle import Obstacle
from flower import Flower
from game_state import State

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "the bee movie"

PLAYER_JUMP_SPEED = 3.5
PLAYER_JUMP_DISTANCE = 5
PLAYER_MOVEMENT_SPEED = 3.5
GRAVITY = 2

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 0
RIGHT_VIEWPORT_MARGIN = 800
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 50


class MyGame(arcade.Window):

    # Main application class

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.bee_sprite = None
        self.bottom_obstacle = None
        self.top_obstacle = None
        self.flower = None

        # lists to keep track of sprites
        self.bottom_obstacles_list = None
        self.top_obstacles_list = None
        self.ground_list = None
        self.flowers_list = None
        self.player_sprite_list = None
        self.physics_engine = None

        # track current state of keys
        self.space_pressed = False

        # keep track of score
        self.score = 0

        # keep track of scrolling
        self.view_left = 0
        self.view_bottom = 0

        self.start_screen = None
        self.start_screen_sprite_list = None
        self.end_screen = None
        self.end_screen_sprite_list = None
        self.y_pressed = False
        self.n_pressed = False
        self.state = State.MAIN_MENU

    def setup_ground(self):
        self.ground_list = arcade.SpriteList()

        for x in range(0, SCREEN_WIDTH + 10, 25):
            ground = arcade.Sprite("sprites/ground.png", 1)
            ground.center_x = x
            ground.center_y = 10
            self.ground_list.append(ground)

    def setup(self):
        # Set up game here. Call this fn to restart game
        self.setup_ground()

        if self.state == State.MAIN_MENU:
            self.start_screen_sprite_list = arcade.SpriteList()
            self.bee_sprite = Bee.setup_bee()
            self.start_screen_sprite_list .append(self.bee_sprite)

            # initiate & place starting screen
            self.start_screen = arcade.Sprite("sprites/start_screen.png", 1)
            self.start_screen.center_x = SCREEN_WIDTH / 2
            self.start_screen.center_y = SCREEN_HEIGHT / 2
            self.start_screen_sprite_list.append(self.start_screen)

        elif self.state == State.PLAYING:
            #initiate sprite lists
            self.bottom_obstacles_list = arcade.SpriteList()
            self.top_obstacles_list = arcade.SpriteList()
            self.flowers_list = arcade.SpriteList()
            self.player_sprite_list = arcade.SpriteList()

            #set up bee
            self.bee_sprite = Bee.setup_bee()
            self.player_sprite_list.append(self.bee_sprite)

            #set up bottom and top obstacles
            self.bottom_obstacles_list, self.top_obstacles_list = Obstacle.setup_obstacles(self.bottom_obstacles_list, self.top_obstacles_list)

            #place flowers for points
            self.flowers_list = Flower.setup(self.flowers_list, self.bottom_obstacles_list, self.top_obstacles_list)

            #set up score
            self.score = 0

            self.physics_engine = arcade.PhysicsEnginePlatformer(self.bee_sprite, self.ground_list, gravity_constant=GRAVITY)

        elif self.state == State.GAME_OVER:
            self.end_screen_sprite_list = arcade.SpriteList()
            self.end_screen = arcade.Sprite("sprites/game_over_screen.png", 1)
            self.end_screen.center_x = SCREEN_WIDTH / 2
            self.end_screen.center_y = SCREEN_HEIGHT / 2
            self.end_screen_sprite_list.append(self.end_screen)

    def on_draw(self):
        # Render the screen
        arcade.start_render()

        self.ground_list.draw()
        if self.state == State.MAIN_MENU:
            self.start_screen_sprite_list.draw()

        elif self.state == State.PLAYING:
            self.player_sprite_list.draw()
            self.bottom_obstacles_list.draw()
            self.top_obstacles_list.draw()
            self.flowers_list.draw()

            score_text = self.score.__str__()
            arcade.draw_text(score_text, 525 + self.view_left, 400 + self.view_bottom, arcade.csscolor.PAPAYA_WHIP, 50)

        elif self.state == State.GAME_OVER:
            self.end_screen_sprite_list.draw()
            self.player_sprite_list.draw()

    def update(self, delta_time):
        if self.state == State.MAIN_MENU:
            if self.space_pressed:
                self.state = State.PLAYING
                self.setup()

        elif self.state == State.PLAYING:
            #game movement
            self.bee_sprite.change_x = 0
            self.bee_sprite.change_y = 0

            if self.space_pressed:
                self.bee_sprite.change_x = PLAYER_JUMP_SPEED
                self.bee_sprite.change_y = PLAYER_JUMP_DISTANCE
            else:
                self.bee_sprite.change_x = PLAYER_MOVEMENT_SPEED

            #check if bee has a flower
            flower_hit_list = arcade.check_for_collision_with_list(self.bee_sprite, self.flowers_list)

            for flower in flower_hit_list:
                flower.remove_from_sprite_lists()
                self.score = self.score + 1

            #check if bee hit an obstacle
            bottom_obstacle_hit_list = arcade.check_for_collision_with_list(self.bee_sprite, self.bottom_obstacles_list)
            top_obstacle_hit_list = arcade.check_for_collision_with_list(self.bee_sprite, self.top_obstacles_list)

            if len(bottom_obstacle_hit_list) != 0 or len(top_obstacle_hit_list) != 0:
                self.bee_sprite.angle = -90
                self.bee_sprite.change_y = 0
                self.state = State.GAME_OVER
                self.setup()

            #kill obstacles & flowers and then make new ones so that it gives "scrolling" effect
            if self.bee_sprite.center_x >= SCREEN_WIDTH:
                self.bee_sprite.center_x = bee.SPRITE_STARTING_X
                Obstacle.kill_obstacles(self.bottom_obstacles_list)
                Obstacle.kill_obstacles(self.top_obstacles_list)
                Obstacle.kill_obstacles(self.flowers_list)

            if len(self.bottom_obstacles_list) == 0 and len(self.top_obstacles_list) == 0:
                self.bottom_obstacles_list, self.top_obstacles_list = Obstacle.setup_obstacles(self.bottom_obstacles_list, self.top_obstacles_list)
                self.flower = Flower.setup(self.flowers_list, self.bottom_obstacles_list, self.top_obstacles_list)

            self.physics_engine.update()

        elif self.state == State.GAME_OVER:
            if self.n_pressed:
                arcade.close_window()

            if self.y_pressed:
                self.state = State.MAIN_MENU
                self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.Y:
            self.y_pressed = True
        elif key == arcade.key.N:
            self.n_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.Y:
            self.y_pressed = False
        elif key == arcade.key.N:
            self.n_pressed = False


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
