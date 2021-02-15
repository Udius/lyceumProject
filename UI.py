import pygame
from pyperclip import paste

from pygame.locals import *

from all_data import *


def makeBrighter(mainColor, extraColor):
    r, g, b = mainColor

    if r + extraColor[0] <= 255:
        r += extraColor[0]
    else:
        r = 255

    if g + extraColor[1] <= 255:
        g += extraColor[1]
    else:
        g = 255

    if b + extraColor[2] <= 255:
        b += extraColor[2]
    else:
        b = 255

    newColor = (r, g, b)
    return newColor


def createText(text, cords, font=fonts['arial']['20'], color=(0, 0, 0), name=None, textDict=texts, alignment=True):
    if name is None:
        name = text
    x, y = cords

    if alignment is True or alignment == 'horizontal':
        x -= font.size(text)[0] // 2
    if alignment is True or alignment == 'vertical':
        y -= font.size(text)[1] // 2

    txt = font.render(text, False, color)
    if textDict is not None:
        textDict[name] = [txt, (x, y)]
    else:
        return [txt, (x, y)]


class UI:
    def __init__(self):
        # {objectName: object}
        self.buttons = dict()
        self.textEdits = dict()
        self.labels = list()

    def update(self):
        for btn in list(self.buttons.values()):
            clickedButton = btn.update()
            if clickedButton is not None:
                return clickedButton

        for tEdit in list(self.textEdits.values()):
            clickedButton = tEdit.update()
            if clickedButton is not None:
                return clickedButton

    def draw(self, surf):
        for btn in list(self.buttons.values()):
            pygame.draw.rect(surf, btn.rectColor, btn.rect)
            pygame.draw.rect(surf, (0, 0, 0), btn.rect, width=2)
            surf.blit(btn.textData[0], btn.textData[1])

        for tEdit in list(self.textEdits.values()):
            pygame.draw.rect(surf, tEdit.rectColor, tEdit.rect)
            pygame.draw.rect(surf, (0, 0, 0), tEdit.rect, width=3)
            surf.blit(tEdit.textData[0], tEdit.textData[1])

    def newButton(self, name, text='', pos=(0, 0), size=(90, 30), rectColor=(0, 0, 0)):
        btn = Button(name, text, pos, size, rectColor=rectColor)
        self.buttons[name] = btn
        return btn

    def newTextEdit(self, name, pos=(0, 0), size=(90, 30), rectColor=(170, 170, 170)):
        tEdit = TextEdit(name, pos, size, rectColor)
        self.textEdits[name] = tEdit
        return tEdit

    def clear(self):
        self.buttons = dict()
        self.textEdits = dict()


class Button(pygame.sprite.Sprite):
    def __init__(self, name, text, pos, size, rectColor=(0, 0, 0)):
        super().__init__()
        self.name = name
        self.text = text
        self.pos = pos
        self.size = size

        self.textColor = (255, 255, 255)
        self.constRectColor = rectColor
        self.rectColor = rectColor

        self.font = fonts['arial']['20']
        self.pressed = self.chosen = False

        self.rect = pygame.Rect(pos, size)
        self.rect.move(pos[0], pos[1])

        txtPos = (self.rect.center[0], self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'Button', textDict=None)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        leftClick = key['mouse'][0]

        # ___ Click's logic ___
        if self.pressed and self.chosen and not leftClick:
            key['mouse'] = (False, False, False)
            self.pressed = self.chosen = False
            return self.name

        if self.rect.collidepoint(mx, my):
            if leftClick:
                self.pressed = True

            self.chosen = True

        else:
            self.chosen = False

        # ___ Button img scale ___
        if self.pressed and self.chosen:
            newColor = makeBrighter(self.constRectColor, (40, 30, 30))
            self.rectColor = newColor

        elif self.chosen:
            newColor = makeBrighter(self.constRectColor, (15, 15, 15))
            self.rectColor = newColor

        else:
            self.rectColor = self.constRectColor

    def setText(self, text, color=(255, 255, 255)):
        self.text = text
        self.textColor = color

        txtPos = (self.rect.center[0], self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'Button', textDict=None)

    def setFont(self, font):
        self.font = font

        txtPos = (self.rect.center[0], self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'Button', textDict=None)

    def move(self, x, y, moveType='topleft'):
        self.pos = (x, y)

        # topleft, topright, center etc.
        if moveType == 'topleft':
            self.rect.topleft = self.pos
        elif moveType == 'topright':
            self.rect.topright = self.pos
        elif moveType == 'bottomleft':
            self.rect.bottomleft = self.pos
        elif moveType == 'bottomright':
            self.rect.bottomright = self.pos
        elif moveType == 'center':
            self.rect.center = self.pos

        txtPos = (self.rect.center[0], self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'Button', textDict=None)


class TextEdit(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, rectColor):
        super().__init__()
        self.name = name
        self.pos = pos
        self.size = size
        self.text = ''

        self.textColor = (0, 0, 0)
        self.constRectColor = rectColor
        self.rectColor = rectColor

        self.font = fonts['arial']['20']
        self.selected = False

        self.rect = pygame.Rect(pos, size)

        txtPos = (self.rect.left + 6, self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'tEdit', textDict=None, alignment='vertical')

    def update(self):
        global textTyping

        mx, my = pygame.mouse.get_pos()
        leftClick = key['mouse'][0]

        # ___ Click's logic ___
        if self.rect.collidepoint(mx, my) and leftClick:
            if not self.selected:
                textTyping[0] = self.text
            self.selected = True

        # ___ Button scale ___
        if self.selected:
            self.typingText()
            newColor = makeBrighter(self.constRectColor, (60, 60, 60))
            self.rectColor = newColor
        else:
            self.rectColor = self.constRectColor

    def typingText(self):
        global lastBackspaceClick
        if self.rect.width - self.font.size(textTyping[0])[0] >= 14:
            self.text = textTyping[0]

            txtPos = (self.rect.left + 6, self.rect.center[1])
            self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'tEdit', textDict=None, alignment='vertical')
        else:
            textTyping[0] = self.text

        if key['lCtrl'] and key['v']:
            self.paste()

        if key['backspace']:
            now = pygame.time.get_ticks() // 10
            if now - lastBackspaceClick >= 10:
                lastBackspaceClick = pygame.time.get_ticks() // 10
                textTyping[0] = textTyping[0][:-1]

    def setText(self, text, color=(0, 0, 0)):
        self.text = text
        self.textColor = color

        txtPos = (self.rect.left + 6, self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'tEdit', textDict=None, alignment='vertical')

    def setFont(self, font):
        self.font = font

        txtPos = (self.rect.left + 6, self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'tEdit', textDict=None, alignment='vertical')

    def move(self, x, y, moveType='topleft'):
        self.pos = (x, y)

        # topleft, topright, center etc.
        if moveType == 'topleft':
            self.rect.topleft = self.pos
        elif moveType == 'topright':
            self.rect.topright = self.pos
        elif moveType == 'bottomleft':
            self.rect.bottomleft = self.pos
        elif moveType == 'bottomright':
            self.rect.bottomright = self.pos
        elif moveType == 'center':
            self.rect.center = self.pos

        txtPos = (self.rect.center[0], self.rect.center[1])
        self.textData = createText(self.text, txtPos, self.font, self.textColor, name=self.text + 'tEdit', textDict=None)

    def clear(self):
        global textTyping

        self.text = ''
        textTyping[0] = ''

    def paste(self):
        global textTyping
        key['lCtrl'] = False
        key['v'] = False

        txt = paste()
        if self.rect.width - self.font.size(txt)[0] >= 14:
            self.text = txt
            textTyping[0] = txt


lastBackspaceClick = pygame.time.get_ticks() // 10