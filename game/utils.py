import random  # Import random function
from pygame.image import load  # Import load function from pygame.image
from pygame.math import Vector2  # Import Vector2 function from pygame.math
from pygame.mixer import Sound  # Import Sound function from pygame.mixer
from pygame import Color  # Import Color function from pygame


def load_sprite(name, with_alpha=True):  # Loads the image
    path = f"assets/images/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):  # Wraps the position of images
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):  # Random position for the asteroids
    return Vector2(random.randrange(surface.get_width()), random.randrange(surface.get_height()),)


def get_random_velocity(min_speed, max_speed):  # Random velocity for the asteroids
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def load_sound(name):  # Load sounds
    path = f"assets/audio/{name}.wav"
    sound = Sound(path)
    sound.set_volume(0.1)
    return sound


def print_text(surface, text, font, color=Color("tomato")):  # Print You Win/You Lose
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)


def print_time(surface, text, font, position, color=Color("tomato")):  # Prints the time
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def get_time():  # Gets the time from the txt
    file = open("assets/shortest_time.txt", "r")
    lowest = file.readline()
    lowest = lowest.split(" ")
    lowest = lowest[0]
    if lowest == "":
        lowest = "-"
    else:
        lowest = int(lowest)
    return lowest
