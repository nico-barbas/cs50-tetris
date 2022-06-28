from enum import Enum, IntEnum
from random import random
import pygame
import sound

from grid import Grid, VALUE_TO_COLOR


class TetrominoKind(IntEnum):
    Invalid = -1
    I = 0
    O = 1
    T = 2
    S = 3
    Z = 4
    J = 5
    L = 6


I = [0, 0, 1, 0,
     0, 0, 1, 0,
     0, 0, 1, 0,
     0, 0, 1, 0]

O = [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 1, 1, 0,
     0, 0, 0, 0]

T = [0, 0, 1, 0,
     0, 1, 1, 0,
     0, 0, 1, 0,
     0, 0, 0, 0]

S = [0, 1, 0, 0,
     0, 1, 1, 0,
     0, 0, 1, 0,
     0, 0, 0, 0]

Z = [0, 0, 1, 0,
     0, 1, 1, 0,
     0, 1, 0, 0,
     0, 0, 0, 0]

J = [0, 0, 0, 0,
     0, 0, 1, 0,
     0, 0, 1, 0,
     0, 1, 1, 0]

L = [0, 0, 0, 0,
     0, 1, 0, 0,
     0, 1, 0, 0,
     0, 1, 1, 0]

KIND_TO_ARRAY = {
    TetrominoKind.I: I,
    TetrominoKind.O: O,
    TetrominoKind.T: T,
    TetrominoKind.S: S,
    TetrominoKind.Z: Z,
    TetrominoKind.J: J,
    TetrominoKind.L: L,
}

KIND_TO_OFFSET = {
    TetrominoKind.I: 0,
    TetrominoKind.O: -1,
    TetrominoKind.T: 0,
    TetrominoKind.S: 0,
    TetrominoKind.Z: 0,
    TetrominoKind.J: -1,
    TetrominoKind.L: -1,
}


class Tetromino:
    def __init__(self, g: Grid) -> None:
        self.x = 0
        self.y = 0
        self.data = [0 for i in range(9)]
        self.kind = TetrominoKind.Invalid
        self.nextKind = TetrominoKind(int(random() * 7))
        self.grid = g
        self.reset()

    def reset(self) -> None:
        nextKind = self.nextKind
        r = int(random() * 7)
        kind = TetrominoKind(r)
        while kind == nextKind:
            r = int(random() * 7)
            kind = TetrominoKind(r)
        self.x = 2
        self.y = KIND_TO_OFFSET[nextKind]
        self.data = KIND_TO_ARRAY[nextKind].copy()
        self.nextKind = kind
        self.kind = nextKind

    def index(self, x: int, y: int) -> int:
        return y*4+x

    def draw(self, screen) -> None:
        (gx, gy) = self.grid.getRenderOffset()
        for y in range(4):
            for x in range(4):
                if self.data[self.index(x, y)] == 1:
                    coord = pygame.Vector2(
                        gx + (self.x + x) * self.grid.cellPixelSize,
                        gy + (self.y + y) * self.grid.cellPixelSize
                    )
                    pygame.draw.rect(
                        screen,
                        VALUE_TO_COLOR[int(self.kind)+1],
                        pygame.Rect(
                            coord.x+1,
                            coord.y+1,
                            self.grid.blockPixelSize,
                            self.grid.blockPixelSize
                        ),
                    )

    def onEvent(self, event) -> None:
        if event == "tick":
            if self.checkCollision(0, 1):
                for y in range(4):
                    for x in range(4):
                        if self.data[self.index(x, y)] == 1:
                            self.grid.setCellCollision(
                                self.x+x, self.y+y,
                                int(self.kind) + 1
                            )

                self.reset()
                self.grid.evalState()
            else:
                self.y += 1
                sound.playSound("tetrominoMoved")
        elif event == "left":
            if not self.checkCollision(-1, 0):
                self.x -= 1
        elif event == "right":
            if not self.checkCollision(1, 0):
                self.x += 1
        elif event == "rotate":
            temp = self.data.copy()
            collision = False
            for y in range(4):
                for x in range(4):
                    temp[self.index(x, y)] = self.data[12+y-(x*4)]
            for y in range(4):
                for x in range(4):
                    index = self.index(x, y)
                    if temp[index] == 1:
                        collision = self.grid.collision(
                            self.x+x,
                            self.y+y,
                        )
                        if collision:
                            break
                if collision:
                    break
            if not collision:
                for i in range(len(temp)):
                    self.data[i] = temp[i]

    def checkCollision(self, offsetX: int, offsetY: int) -> bool:
        for y in range(4):
            for x in range(4):
                index = self.index(x, y)
                if self.data[index] == 1:
                    collision = self.grid.collision(
                        self.x+x+offsetX,
                        self.y+y+offsetY,
                    )
                    if collision:
                        return collision