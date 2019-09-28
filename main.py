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
       # TODO: keep track of everything happening in the game
    
    def on_key_press(self, key, modifiers):
        # TODO: keep track of which key has been pressed!

    def on_key_release(self, key, modifiers):
        # TODO: keep track of which key has been released!


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
