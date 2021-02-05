import os, sys
import pygame, requests

from pygame.locals import *

from all_data import *


def terminate():
    pygame.quit()
    if os.path.isfile(map_file):
        os.remove(map_file)
    sys.exit(1)


def checkEvent():
    global zoom

    image = None
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                key['top'] = True
            elif event.key == K_DOWN:
                key['bottom'] = True
            elif event.key == K_LEFT:
                key['left'] = True
            elif event.key == K_RIGHT:
                key['right'] = True

        elif event.type == KEYUP:
            if event.key == K_UP:
                key['top'] = False
            elif event.key == K_DOWN:
                key['bottom'] = False
            elif event.key == K_LEFT:
                key['left'] = False
            elif event.key == K_RIGHT:
                key['right'] = False

        elif event.type == MOUSEBUTTONDOWN and 0 < zoom < 20:
            if event.button == 4:
                if zoom < 0.05:
                    zoom -= 0.0005
                elif zoom < 0.1:
                    zoom -= 0.01
                elif zoom < 0.3:
                    zoom -= 0.05
                elif zoom < 0.6:
                    zoom -= 0.1
                elif zoom < 2:
                    zoom -= 0.3

                image = getMap()
            elif event.button == 5:
                if zoom < 0.05:
                    zoom += 0.0005
                elif zoom < 0.1:
                    zoom += 0.01
                elif zoom < 0.3:
                    zoom += 0.05
                elif zoom < 0.6:
                    zoom += 0.1
                elif zoom < 2:
                    zoom += 0.3

                image = getMap()
    return image


def getMap():
    cords = ','.join(mapCords)
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={cords}&spn={str(zoom)},{str(zoom)}&l={mapType}&size=650,450"
    print(zoom)
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        terminate()
    else:

        with open(map_file, "wb") as file:
            file.write(response.content)

        image = pygame.image.load(map_file)

    return image


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Lyceum project')

image = getMap()

while True:
    newImage = checkEvent()

    speed = [0, 0]
    if key['left']:
        speed[0] -= 0.5 * zoom
    if key['right']:
        speed[0] += 0.5 * zoom
    if key['top']:
        speed[1] += 0.5 * zoom
    if key['bottom']:
        speed[1] -= 0.5 * zoom

    if speed != [0, 0] or newImage is not None:
        mapCords[0] = str(float(mapCords[0]) + speed[0])
        mapCords[1] = str(float(mapCords[1]) + speed[1])
        image = getMap()

    # Drawing
    screen.blit(image, (0, 0))

    # Flip & wait
    pygame.display.update()
    clock.tick(FPS)
