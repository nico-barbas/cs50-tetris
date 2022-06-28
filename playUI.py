from menu import Button
from grid import VALUE_TO_COLOR
import sound
import pygame
from enum import IntEnum

MENU_CLR = pygame.Color(48, 41, 51, 255)


class GameOverItem(IntEnum):
    Replay = 0
    Exit = 1


class PlayUI:
    def __init__(self, font) -> None:
        self.gameOverActive = False
        self.selectAvailable = True
        self.selectTimer = 0
        self.selectRate = 0.1
        self.gameOverText = [
            [
                1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0,
                1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0,
                1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,
            ],
            [
                1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1,
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0,
                1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
            ],
        ]

        (ww, wh) = pygame.display.get_window_size()
        self.gameOverRect = pygame.Rect(
            ww/2 - (ww-100)/2,
            wh/2 - (200)/2,
            ww-100,
            200
        )
        self.cellSize = 6
        self.blockSize = self.cellSize - 1
        self.gameOverTextPos = pygame.Vector2(
            self.gameOverRect.x +
            (self.gameOverRect.width - (15 * self.cellSize))/2,
            self.gameOverRect.y + 4
        )
        o = 20
        self.titleHeight = (4 * self.cellSize + 8) * 2
        self.gameOverSelected = GameOverItem.Replay
        self.gameOverBtns = [
            Button(self.gameOverRect, self.titleHeight + o, font, "REPLAY"),
            Button(self.gameOverRect, self.titleHeight + o*3, font, "EXIT"),
        ]
        self.gameOverBtns[self.gameOverSelected].select()
        self.gameOverReplayPressed = False
        self.gameOverExitPressed = False

    def reset(self):
        self.gameOverActive = False
        self.gameOverReplayPressed = False
        self.gameOverSelected = GameOverItem.Replay

    def update(self, dt):
        if self.gameOverActive:
            if self.selectAvailable:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.gameOverBtns[self.gameOverSelected].deselect()
                    self.gameOverSelected = (self.gameOverSelected - 1) % 2
                    self.gameOverBtns[self.gameOverSelected].select()
                    self.selectAvailable = False
                    sound.playSound("uiMove")
                elif keys[pygame.K_s]:
                    self.gameOverBtns[self.gameOverSelected].deselect()
                    self.gameOverSelected = (self.gameOverSelected + 1) % 2
                    self.gameOverBtns[self.gameOverSelected].select()
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

    def draw(self, screen):
        if self.gameOverActive:
            pygame.draw.rect(
                screen,
                MENU_CLR,
                self.gameOverRect
            )
            pygame.draw.rect(
                screen,
                (255, 255, 255, 255),
                self.gameOverRect,
                1
            )

            # Draw game over text
            yoffset = 0
            for word in self.gameOverText:
                for y in range(4):
                    for x in range(15):
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

                        if word[y*15+x] == 1:
                            rect = pygame.Rect(
                                self.gameOverTextPos.x + x * self.cellSize,
                                self.gameOverTextPos.y + y * self.cellSize + yoffset,
                                self.blockSize, self.blockSize
                            )
                            pygame.draw.rect(
                                screen,
                                clr,
                                rect
                            )

                yoffset += 4 * self.cellSize + 4
            # Draw all the current Buttons
            for btn in self.gameOverBtns:
                btn.draw(screen, VALUE_TO_COLOR[self.gameOverSelected+1])

    def onItemSelected(self):
        if self.gameOverSelected == GameOverItem.Replay:
            self.gameOverReplayPressed = True
        elif self.gameOverSelected == GameOverItem.Exit:
            self.gameOverExitPressed = True
