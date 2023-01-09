from pygame.math import Vector2  # Import function Vector2 from pygame.math
from pygame.transform import rotozoom  # Import function rotozoom from pygame.transform
from utils import get_random_velocity, load_sound, load_sprite, wrap_position  # Import functions from utils.py
UP = Vector2(0, -1)


class GameObject:  # Class for all game objects
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.click = 0

    def draw(self, surface):  # Draw game objects
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):  # Change position of objects
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):  # Check if an object collides with one another
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):  # A child class of GameObject, for the spaceship
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):  # Rotates spaceship
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):  # Draws spaceship
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):  # Increase the speed of spaceship
        self.velocity += self.direction * self.ACCELERATION
        self.click += 1

    def decelerate(self):  # Decrease the speed of spaceship
        if self.click > 0:
            self.velocity -= self.direction * self.ACCELERATION
            self.click -= 1

    def shoot(self):  # Shoot lasers
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Asteroid(GameObject):  # A child class of GameObject, for the asteroid
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        size_to_scale = {3: 1, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):  # Split the asteroid into smaller pieces
        if self.size > 1:
            for i in range(2):
                asteroid = Asteroid(self.position, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):  # A child class of GameObject, for the bullet
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):  # Change position of bullets
        self.position = self.position + self.velocity
