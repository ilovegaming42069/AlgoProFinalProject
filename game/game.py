import pygame  # Module used in this project
from utils import get_random_position, load_sprite, print_text, print_time, get_time  # Import functions from utils.py
from models import Asteroid, Spaceship  # Import classes from models.py


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    NUMBER_ASTEROID = 6
    FPS = 60

    def __init__(self):
        self._init_pygame()

        self.finish = False
        self.playing = True
        self.duration = 180

        self.screen = pygame.display.set_mode((800, 600))
        # Screen with 800*600 pixels in default
        self.timer = 0

        self.font = pygame.font.Font(None, 64)

        self.background = load_sprite("space", False)  # Loads the image

        self.boom = pygame.mixer.Sound("assets/audio/explosion.wav")  # Sound effect
        self.boom.set_volume(0.1)

        self.clock = pygame.time.Clock()
        self.message = ""
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for i in range(SpaceRocks.NUMBER_ASTEROID):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):  # The main loop of the game
        pygame.mixer.music.load("assets/audio/menu.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.menu()
        pygame.mixer.music.load("assets/audio/game_music.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        while self.playing:
            self._handle_input()  # Input handling
            self._process_game_logic()  # Game logic
            self._draw()  # Drawing
            if self.finish:
                self.duration -= 1
                if self.duration == 0:
                    self.playing = False

    def _init_pygame(self):
        self.best_time = get_time()
        pygame.init()
        pygame.display.set_caption("Space Rocks")  # Name of the game

    def menu(self):  # Menu/beginning section of the game
        title = self.font.render("Space Rocks", True, (255, 100, 50))

        play = pygame.image.load('assets/images/start.png')
        play = pygame.transform.scale(play, (200, 100))

        ext = pygame.image.load('assets/images/exit.png')
        ext = pygame.transform.scale(ext, (225, 135))

        box = pygame.image.load('assets/images/box.png')
        box = pygame.transform.scale(box, (525, 100))

        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(box, (150, 30))
            self.screen.blit(title, (275, 60))
            self.screen.blit(play, (300, 250))
            self.screen.blit(ext, (290, 350))

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    press = pygame.mouse.get_pressed()
                    if press[0]:
                        if 300 < mouse[0] < 500 and 250 < mouse[1] < 350:
                            return
                        elif 300 < mouse[0] < 500 and 350 < mouse[1] < 450:
                            quit()

            pygame.display.update()

    def paused(self):  # Pausing the game
        title = self.font.render("Paused", True, (255, 100, 50))

        resume = pygame.image.load('assets/images/resume.png')  # Loads resume button
        resume = pygame.transform.scale(resume, (200, 100))

        back = pygame.image.load('assets/images/back.png')  # Loads back button
        back = pygame.transform.scale(back, (175, 75))

        ext = pygame.image.load('assets/images/exit.png')  # Loads exit button
        ext = pygame.transform.scale(ext, (225, 135))

        box = pygame.image.load('assets/images/box.png')
        box = pygame.transform.scale(box, (525, 100))

        while True:
            start = False
            # Draws the images
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(box, (150, 30))
            self.screen.blit(title, (325, 60))
            self.screen.blit(resume, (300, 150))
            self.screen.blit(back, (310, 275))
            self.screen.blit(ext, (290, 350))

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        start = True
                        break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    press = pygame.mouse.get_pressed()  # return list [left, right, middle]
                    if press[0]:  # Left click
                        if 300 < mouse[0] < 500 and 150 < mouse[1] < 250:
                            start = True
                            break
                        elif 300 < mouse[0] < 500 and 250 < mouse[1] < 350:
                            start = True
                            self.playing = False
                            break
                        elif 300 < mouse[0] < 500 and 350 < mouse[1] < 450:
                            quit()
            if start:
                break
            pygame.display.update()

    def _handle_input(self):  # Input Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()

            is_key_pressed = pygame.key.get_pressed()
            if self.spaceship:
                if is_key_pressed[pygame.K_RIGHT]:
                    self.spaceship.rotate(clockwise=True)
                elif is_key_pressed[pygame.K_LEFT]:
                    self.spaceship.rotate(clockwise=False)
                elif is_key_pressed[pygame.K_UP]:
                    self.spaceship.accelerate()
                elif is_key_pressed[pygame.K_DOWN]:
                    self.spaceship.decelerate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused()

    def _process_game_logic(self):  # Game Logic
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.boom.play()
                    self.spaceship = None
                    self.message = "You lost!"
                    self.finish = True
                    break
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.boom.play()
                    break

        if not self.asteroids and self.spaceship:
            self.message = "You won!"
            self.finish = True

            if self.best_time == "-" or self.timer//SpaceRocks.FPS < int(self.best_time):
                file = open("assets/shortest_time.txt", "w")
                file.write(f"{self.timer//SpaceRocks.FPS} seconds")
                file.close()

    def _draw(self):  # Draw the images
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        if self.finish and self.spaceship:
            new_best_time = self.font.render(f"New best time: {self.timer // SpaceRocks.FPS} seconds", True, (255, 100, 50))
            self.screen.blit(new_best_time, (100, 200))

        time_font = pygame.font.Font(None, 32)
        print_time(self.screen, f"Best Time: {self.best_time} seconds", time_font, (10, 10))

        if self.asteroids and self.spaceship:
            self.timer += 1

        print_time(self.screen, f"Time: {self.timer//SpaceRocks.FPS} seconds", time_font, (10, 40))
        pygame.display.flip()
        self.clock.tick(SpaceRocks.FPS)

    def _get_game_objects(self):  # Return game objects
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
