from grid import VALUE_TO_COLOR
import sound
from enum import IntEnum
import pygame


class MenuItem(IntEnum):
    Play = 0
    Settings = 1
    Exit = 2


class Menu:
    def __init__(self, font: pygame.font.Font) -> None:
        self.selected = MenuItem.Play
        self.selectAvailable = True
        self.selectTimer = 0
        self.selectRate = 0.1
        self.playPressed = False
        self.exitPressed = False

        (ww, wh) = pygame.display.get_window_size()
        self.rect = pygame.Rect(ww/2 - 100, wh/2 - 250/2 - 5, 200, 250)

        self.cellSize = 6
        self.blockSize = self.cellSize - 1
        self.title = [
            1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1,
            0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0,
            0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1,
            0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,
        ]

        self.titlePos = pygame.Vector2(
            self.rect.x + (self.rect.width - (21 * self.cellSize))/2,
            self.rect.y + 4,
        )
        self.titleHeight = 4 * self.cellSize + 8
        o = 50
        self.btns = [
            Button(self.rect, self.titleHeight + o, font, "PLAY"),
            Button(self.rect, self.titleHeight + o*2, font, "SETTINGS"),
            Button(self.rect, self.titleHeight + o*3, font, "EXIT"),
        ]
        self.btns[self.selected].select()

    def update(self, dt):
        if self.selectAvailable:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.btns[self.selected].deselect()
                self.selected = (self.selected - 1) % 3
                self.btns[self.selected].select()
                self.selectAvailable = False
                sound.playSound("uiMove")
            elif keys[pygame.K_s]:
                self.btns[self.selected].deselect()
                self.selected = (self.selected + 1) % 3
                self.btns[self.selected].select()
                self.selectAvailable = False
                sound.playSound("uiMove")

            #
            if keys[pygame.K_SPACE]:
                self.onItemSelected()
        else:
            self.selectTimer += dt
            if self.selectTimer >= self.selectRate:
                self.selectAvailable = True
                self.selectTimer = 0

    def draw(self, screen: pygame.Surface):
        self.drawTitle(screen)

        # Draw the outline of the menu
        pygame.draw.rect(
            screen,
            (255, 255, 255, 255),
            pygame.Rect(self.rect.x, self.rect.y,
                        self.rect.width, self.titleHeight),
            1
        )
        pygame.draw.rect(screen, pygame.Color(
            255, 255, 255, 255), self.rect, 1)

        # Draw all the current Buttons
        for btn in self.btns:
            btn.draw(screen, VALUE_TO_COLOR[self.selected+1])

    def drawTitle(self, screen):
        for y in range(4):
            for x in range(21):
                if self.title[y*21+x] == 1:
                    clr = pygame.Color(255, 255, 255, 255)
                    if x <= 3:
                        clr = VALUE_TO_COLOR[5]
                    elif x >= 4 and x <= 7:
                        clr = VALUE_TO_COLOR[7]
                    elif x >= 8 and x <= 11:
                        clr = VALUE_TO_COLOR[2]
                    elif x >= 12 and x <= 15:
                        clr = VALUE_TO_COLOR[4]
                    elif x >= 16 and x <= 17:
                        clr = VALUE_TO_COLOR[1]
                    elif x >= 18 and x <= 21:
                        clr = VALUE_TO_COLOR[3]
                    rect = pygame.Rect(
                        self.titlePos.x + x * self.cellSize,
                        self.titlePos.y + y * self.cellSize,
                        self.blockSize, self.blockSize
                    )
                    pygame.draw.rect(
                        screen,
                        clr,
                        rect
                    )

    def onItemSelected(self):
        sound.playSound("uiSelect")
        if self.selected == MenuItem.Play:
            self.playPressed = True
        elif self.selected == MenuItem.Exit:
            self.exitPressed = True


class Button:
    def __init__(self, pRect: pygame.Rect, yoffset: float, font: pygame.font.Font, text) -> None:
        self.clr = pygame.Color(255, 255, 255, 255)
        self.text = font.render(text, True, self.clr)
        (w, h) = font.size(text)
        self.rect = pygame.Rect(
            pRect.x + (pRect.width - w) / 2,
            pRect.y + yoffset,
            w,
            h,
        )
        self.selected = False

    def draw(self, screen, selectClr: pygame.Color):
        screen.blit(self.text, (self.rect.x, self.rect.y))
        if self.selected:
            pygame.draw.rect(screen, selectClr, self.rect, 1)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
