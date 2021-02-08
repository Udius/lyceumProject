import pygame
import os, sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data\\images', name)
    if not os.path.isfile(fullname):
        print(f"[ERROR] No such file: '{fullname}'")
        terminate()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image.set_colorkey(colorkey)
            image = image.convert_alpha()

    return image


WIDTH = 650
HEIGHT = 450
FPS = 60

mapCords = ['37.6156', '55.7522']
mapType = 'map'
speed = [0, 0]
zoom = 1

all_UI = pygame.sprite.Group()

# Клавиши стрелок: если нажаты, то будет True
key = {
    'top': False,
    'left': False,
    'right': False,
    'bottom': False,
    '1': False,
    '2': False,
    '3': False
}

ui_images = {
    'search': load_image('search.png')
}

# ---< FILES >---
map_file = "map.png"
