import os
import sys

import pygame
import requests

from all_data import *


def terminate():
    pygame.quit()
    os.remove(map_file)
    sys.exit(1)


pygame.init()
screen = pygame.display.set_mode((600, 450))

response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    terminate()

with open(map_file, "wb") as file:
    file.write(response.content)

while True:
    if pygame.event.wait().type == pygame.QUIT:
        terminate()

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
