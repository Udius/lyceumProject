import os, sys
import pygame, requests

from pygame.locals import *

from all_data import *
from all_classes import *


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
            elif event.key == K_1:
                key['1'] = True
            elif event.key == K_2:
                key['2'] = True
            elif event.key == K_3:
                key['3'] = True

        elif event.type == KEYUP:
            if event.key == K_UP:
                key['top'] = False
            elif event.key == K_DOWN:
                key['bottom'] = False
            elif event.key == K_LEFT:
                key['left'] = False
            elif event.key == K_RIGHT:
                key['right'] = False
            elif event.key == K_1:
                key['1'] = True
            elif event.key == K_2:
                key['2'] = True
            elif event.key == K_3:
                key['3'] = True

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

Button('search', (WIDTH - 80, HEIGHT - 32))

image = getMap()

while True:
    newImage = checkEvent()

    '''
    Работаем с клавишами
    '''
    speed = [0, 0]
    if key['left']:
        speed[0] -= 0.5 * zoom
    if key['right']:
        speed[0] += 0.5 * zoom
    if key['top']:
        speed[1] += 0.5 * zoom
    if key['bottom']:
        speed[1] -= 0.5 * zoom

    if key['1']:
        mapType = 'map'
        image = getMap()
    elif key['2']:
        mapType = 'sat'
        image = getMap()
    elif key['3']:
        mapType = 'sat,trf,skl'
        image = getMap()

    '''
    Обновляем все спрайты
    '''

    all_UI.update()

    '''
    Запрос на новую карту, если мы перемещаемся, или карты нету впринципе
    '''
    if speed != [0, 0] or newImage is not None:
        mapCords[0] = str(float(mapCords[0]) + speed[0])
        mapCords[1] = str(float(mapCords[1]) + speed[1])
        image = getMap()

    # Drawing
    screen.blit(image, (0, 0))
    all_UI.draw(screen)

    # Flip & wait
    pygame.display.update()
    clock.tick(FPS)
