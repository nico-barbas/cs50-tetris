from ast import Import
from typing import Tuple
import pygame
from pygame import Color

LINE_WIDTH = 1

VALUE_TO_COLOR = [
    None,
    Color(114, 194, 200),  # I
    Color(210, 210, 137),  # O
    Color(185, 90, 187),  # T
    Color(105, 158, 100),  # S
    Color(188, 41, 76),   # Z
    Color(60, 66, 152),   # J
    Color(207, 119, 84),  # L
]


class Grid:
    def __init__(self, onGameLost, onLineScored) -> None:
        (_, wh) = pygame.display.get_window_size()

        self.width = 10
        self.height = 20
        self.cellPixelSize = 18
        self.blockPixelSize = self.cellPixelSize - LINE_WIDTH
        self.pixelWidth = self.width * self.cellPixelSize
        self.pixelHeight = self.height * self.cellPixelSize
        self.x = 10
        self.y = (wh - self.pixelHeight) / 2
        self.lineColor = pygame.Color(255, 255, 255, 255)
        self.data = [0 for i in range(self.width*self.height)]
        self.loseCallback = onGameLost
        self.scoreCallback = onLineScored

    def reset(self):
        self.data = [0 for i in range(self.width*self.height)]

    def draw(self, screen) -> None:
        pygame.draw.rect(
            screen,
            self.lineColor,
            pygame.Rect(
                self.x, self.y,
                self.pixelWidth+1, self.pixelHeight+1
            ),
            1,
        )

        for y in range(self.height):
            for x in range(self.width):
                if self.data[y*self.width+x] > 0:
                    coord = pygame.Vector2(
                        self.x + x * self.cellPixelSize,
                        self.y + y * self.cellPixelSize
                    )
                    pygame.draw.rect(
                        screen,
                        VALUE_TO_COLOR[self.data[y*self.width+x]],
                        pygame.Rect(
                            coord.x+1,
                            coord.y+1,
                            self.blockPixelSize,
                            self.blockPixelSize
                        ),
                    )

    def collision(self, x: int, y: int) -> bool:
        return x < 0 or x >= self.width or y >= self.height or self.data[y*self.width+x] > 0

    def setCellCollision(self, x: int, y: int, value: int):
        self.data[y*self.width+x] = value

    def getRenderOffset(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def evalState(self) -> bool:
        for i in range(self.width):
            if self.data[i] > 0:
                self.loseCallback()

        # check the rest of the board for full lines
        lineScore = 0
        for y in range(self.height):
            fullLine = True
            for x in range(self.width):
                if self.data[y*self.width+x] == 0:
                    fullLine = False
                    break
            if fullLine:
                # increment the line scored count
                lineScore += 1
                # move every tile by 1 on the Y axis
                for z in range(y, 1, -1):
                    for x in range(self.width):
                        self.data[z*self.width +
                                  x] = self.data[(z-1)*self.width+x]
        if lineScore > 0:
            self.scoreCallback(lineScore)
