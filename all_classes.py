from all_data import *


class Button(pygame.sprite.Sprite):
    def __init__(self, name, cords):
        super().__init__(all_UI)
        self.absImage = ui_images[name]
        self.image = self.absImage
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.pressed = False
        self.name = name

    def update(self):
        mPos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mPos) and (mousePress or self.pressed):
            self.pressed = True
            oldPos = self.rect.center
            w, h, = self.absImage.get_width(), self.absImage.get_height()
            self.image = pygame.transform.scale(self.absImage, (int(w * 0.95), int(h * 0.95)))
            self.rect = self.image.get_rect()
            self.rect.center = oldPos
            if not mousePress:
                self.pressed = False
                return True
        else:
            self.pressed = False
            oldPos = self.rect.center
            self.image = self.absImage
            self.rect = self.image.get_rect()
            self.rect.center = oldPos

        return False

    def move(self, x, y):
        self.rect.center = x, y
