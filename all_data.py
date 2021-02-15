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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Lyceum project')

mapCords = ['37.6156', '55.7522']
mapType = 'map'
speed = [0, 0]
zoom = 1
texts = list()
textTyping = ['']

# Клавиши стрелок: если нажаты, то будет True
key = {
    'top': False,
    'left': False,
    'right': False,
    'bottom': False,
    '1': False,
    '2': False,
    '3': False,
    'lCtrl': False,
    'backspace': False,
    'v': False,
    'mouse': (False, False, False)
}

ui_images = {
    'search': load_image('search.png')
}

# ---< FILES >---
map_file = "map.png"

fonts = {
    'arial': {
        '20': pygame.font.SysFont('arial', 20),
        '22': pygame.font.SysFont('arial', 22),
        '28': pygame.font.SysFont('arial', 28)
    }
}
