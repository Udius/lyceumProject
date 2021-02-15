import os, sys
import pygame, requests

from pygame.locals import *

from all_data import *
from UI import *


def terminate():
    pygame.quit()
    if os.path.isfile(map_file):
        os.remove(map_file)
    sys.exit(1)


def checkEvent():
    global zoom, lastBackspaceClick
    key['mouse'] = pygame.mouse.get_pressed()

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
            elif event.key == K_LCTRL:
                key['lCtrl'] = True
            elif event.key == K_v:
                key['v'] = True

            if event.key == K_BACKSPACE:
                key['backspace'] = True
            elif event.unicode.isalnum() or event.unicode in ' .,;:"<>':
                '''
                Using in UI.tEdit
                '''
                textTyping[0] += event.unicode

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
                key['1'] = False
            elif event.key == K_2:
                key['2'] = False
            elif event.key == K_3:
                key['3'] = False
            elif event.key == K_LCTRL:
                key['lCtrl'] = False
            elif event.key == K_v:
                key['v'] = False
            elif event.key == K_BACKSPACE:
                key['backspace'] = False

        elif event.type == MOUSEBUTTONDOWN and 0 < zoom < 20:
            if event.button == 4:
                if zoom < 0.01:
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
                if zoom < 0.01:
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


ui = UI()

btn = ui.newButton('search', 'Search', (WIDTH - 130, HEIGHT - 50), size=(110, 35), rectColor=(40, 40, 40))
btn.setFont(fonts['arial']['28'])

tEdit = ui.newTextEdit('searchData', (WIDTH - 460, HEIGHT - 50), size=(310, 35))
tEdit.setFont(fonts['arial']['22'])

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

    if key['lCtrl'] and key['1']:
        mapType = 'map'
        image = getMap()
        key['1'] = False
    elif key['lCtrl'] and key['2']:
        mapType = 'sat'
        image = getMap()
        key['2'] = False
    elif key['lCtrl'] and key['3']:
        mapType = 'sat,trf,skl'
        image = getMap()
        key['3'] = False

    '''
    Работа с интерфейсом
    '''

    clickedButton = ui.update()
    if clickedButton == 'search':
        print('Search button clicked')

    '''
    Запрос на новую карту, если мы перемещаемся, или карты нету впринципе
    '''
    if speed != [0, 0] or newImage is not None:
        mapCords[0] = str(float(mapCords[0]) + speed[0])
        mapCords[1] = str(float(mapCords[1]) + speed[1])
        image = getMap()

    # Drawing
    screen.blit(image, (0, 0))
    ui.draw(screen)

    # Flip & wait
    pygame.display.update()
    clock.tick(FPS)
