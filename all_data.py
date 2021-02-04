WIDTH = 1024
HEIGHT = 720

mapCoords = '37.6156,55.7522'

map_request = f"http://static-maps.yandex.ru/1.x/?ll={mapCoords}&spn=0.5,0.5&l=map"

# Клавиши стрелок: если нажаты, то будет True
key = {
    'top': False,
    'left': False,
    'right': False,
    'bottom': False
}
