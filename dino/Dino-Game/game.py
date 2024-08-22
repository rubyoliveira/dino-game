import uvage
import random

class Game:
    def __init__(self):
        """
        Initializes the Game class.
        Sets up the game window, loads images, and initializes game elements.
        """
        # Set up the game window
        self.camera = uvage.Camera(800, 600)

        # Load images
        self.dino_images = uvage.load_sprite_sheet('dino_sprite.png', 1, 2)
        self.ground_image = 'ground.png'
        self.cloud_image = 'cloud.png'
        self.cactus_images = [
            'cactus_small.png', 'cactus_big.png', 'cactus_patch2small.png',
            'cactus_patch2big.png', 'cactus_mixed_patch.png', 'cactus_patch3.png'
        ]

        # Initialize game elements
        self.dino = uvage.from_image(35, 370, self.dino_images[0])
        self.current_frame = 0

        self.obstacles = []
        self.grounds = []
        self.clouds = []

        self.score = 0
        self.game_over = False
        self.game_on = False

        self.obstacle_speed = 8
        self.character_speed = 20
        self.score_font_size = 24

    def move_dino(self):
        """
        Handles the movement and animation of the dino.
        Updates the dino's position based on user input and gravity, and changes its sprite image for animation.
        """
        if self.game_on:
            if uvage.is_pressing('space') and self.dino.y >= 370:
                self.dino.y = 270
            if self.dino.y >= 270 and self.dino.y < 370:
                self.dino.speedy += 0.53
                self.dino.move_speed()
            if self.dino.y >= 370:
                self.dino.speedy = 0
                self.dino.move_speed()

            self.current_frame += 0.8
            self.score += 0.25
            if self.current_frame >= len(self.dino_images):
                self.current_frame = 0
            self.dino.image = self.dino_images[int(self.current_frame)]
        else:
            self.dino.image = self.dino_images[-1]

    def manage_clouds(self):
        """
        Manages the cloud objects in the game.
        Adds new clouds, removes off-screen clouds, and moves clouds if the game is on.
        """
        if len(self.clouds) == 0:
            cloud1 = uvage.from_image(900, 200, self.cloud_image)
            self.clouds.append(cloud1)

        for cloud in self.clouds:
            cloud_x = random.randint(0, 400)
            cloud_y = random.randint(0, 200)

            if cloud.x == 400:
                self.clouds.append(uvage.from_image(800 + cloud_x, cloud_y, self.cloud_image))

            if cloud.x == -100:
                self.clouds.pop(self.clouds.index(cloud))

            if self.game_on and not self.game_over:
                cloud.speedx = -1
                cloud.move_speed()

            self.camera.draw(cloud)

    def manage_ground(self):
        """
        Manages the ground objects in the game.
        Adds new ground sections, removes off-screen ground sections, and moves ground if the game is on.
        """
        if len(self.grounds) == 0:
            ground1 = uvage.from_image(400, 400, self.ground_image)
            ground2 = uvage.from_image(1200, 400, self.ground_image)
            self.grounds.append(ground1)
            self.grounds.append(ground2)

        for ground in self.grounds:
            if ground.x == 0:
                self.grounds.append(uvage.from_image(1200, 400, self.ground_image))

            if self.game_on and not self.game_over:
                ground.speedx = -self.obstacle_speed
                ground.move_speed()

            self.camera.draw(ground)

    def manage_obstacles(self):
        """
        Manages the obstacle objects in the game.
        Adds new obstacles, removes off-screen obstacles, moves obstacles if the game is on, and checks for collisions with the dino.
        """
        obstacle_list = [uvage.from_image(850, 390, img) for img in self.cactus_images]

        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_list[0])

        for obstacle in self.obstacles:
            cactus_random = random.randint(0, 5)
            if obstacle.x == 450:
                self.obstacles.append(obstacle_list[cactus_random])
            if obstacle.x == -20:
                self.obstacles.pop(self.obstacles.index(obstacle))

            if self.game_on and not self.game_over:
                obstacle.speedx = -self.obstacle_speed
                obstacle.move_speed()
                if self.dino.touches(obstacle, -15, -15):
                    self.dino.move_to_stop_overlapping(obstacle)
                    self.game_over = True

            self.camera.draw(obstacle)

    def main_game(self):
        """
        Manages the main game logic.
        Displays instructions, starts the game, handles game over and restart, and draws the score.
        """
        if not self.game_on and not self.game_over:
            self.camera.draw(uvage.from_text(400, 260, 'Press the S Key to Start the Game', 30, 'darkgrey'))

        if self.score <= 20 and self.game_on:
            self.camera.draw(uvage.from_text(400, 260, 'Press the Space Key to Jump Over Moving Obstacles', 30, 'darkgrey'))

        if uvage.is_pressing('s'):
            self.game_on = True

        self.manage_clouds()
        self.manage_ground()
        self.manage_obstacles()

        if self.game_over:
            self.game_on = False
            self.camera.draw(uvage.from_text(400, 250, 'Game Over', 40, 'darkgrey'))
            self.camera.draw(uvage.from_text(400, 280, 'Press the R Key to Restart', 30, 'darkgrey'))

        if uvage.is_pressing('r') and self.game_over:
            self.reset_game()

        self.camera.draw(uvage.from_text(40, 10, "Score: " + str(int(self.score)), self.score_font_size, "darkgrey"))

    def reset_game(self):
        """
        Resets the game to its initial state.
        Clears obstacles, clouds, and grounds, resets the score and dino position, and sets game state flags.
        """
        self.obstacles.clear()
        self.clouds.clear()
        self.grounds.clear()
        self.score = 0
        self.dino.x = 35
        self.dino.y = 370
        self.game_on = True
        self.game_over = False

    def tick(self):
        """
        Game loop tick function to update and render game elements.
        Clears the camera, runs the main game logic, moves the dino, draws the dino, and updates the display.
        """
        self.camera.clear('navajowhite')
        self.main_game()
        self.move_dino()
        self.camera.draw(self.dino)
        self.camera.display()
