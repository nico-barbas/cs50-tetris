from enum import Enum
from tetromino import Tetromino, KIND_TO_ARRAY
from input import PlayerInput
from grid import Grid, VALUE_TO_COLOR
from menu import Menu
import sound
from playUI import PlayUI
import time
import pygame.font
import pygame


CLEAR_COLOR = pygame.Color(48, 41, 51, 255)


class GameState(Enum):
    Menu = 0
    Play = 1


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((300, 400))
        self.running = True
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.font = pygame.font.Font("assets/monogram.ttf", 24)
        self.state = GameState.Menu

        # Game data
        self.menu = Menu(self.font)
        self.grid: Grid = Grid(self.onGameLost, self.onLineScored)
        self.tetromino = Tetromino(self.grid)
        self.playerInput = PlayerInput()
        self.playUI = PlayUI(self.font)
        self.gamePaused = False

        self.playerInput.addListener(self.tetromino)
        self.playerScore = 0
        self.playerLevel = 0
        self.lineCounter = 0
        self.lastLineScore = 0

    def onGameLost(self):
        self.gamePaused = True
        self.playUI.gameOverActive = True

    def reset(self):
        self.grid.reset()
        self.tetromino.reset()
        self.playerInput.reset()
        self.playUI.reset()
        self.playerScore = 0
        self.lastLineScore = 0
        self.lineCounter = 0
        self.gamePaused = False

    def onLineScored(self, amount: int):
        if amount == 1:
            self.playerScore += 100
        if amount == 2:
            self.playerScore += 300
        if amount == 3:
            self.playerScore += 500
        if amount == 4:
            if self.lastLineScore == 4:
                self.playerScore += 1200
            else:
                self.playerScore += 800
        self.lastLineScore = amount

        self.lineCounter += amount
        if self.lineCounter >= 10:
            self.lineCounter -= 10
            self.playerLevel += 1
            if self.playerLevel <= 9:
                self.playerInput.increaseTickRate()
            elif self.playerLevel == 10:
                self.playerInput.increaseTickRate()
            elif self.playerLevel == 13:
                self.playerInput.increaseTickRate()
            elif self.playerLevel == 16:
                self.playerInput.increaseTickRate()
            elif self.playerLevel == 19:
                self.playerInput.increaseTickRate()
            elif self.playerLevel == 29:
                self.playerInput.increaseTickRate()
        sound.playSound("lineScored")

    def run(self):
        while self.running:
            dt = time.time() - self.last_time
            self.last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.state == GameState.Menu:
                self.menu.update(dt)
                if self.menu.playPressed:
                    self.state = GameState.Play
                elif self.menu.exitPressed:
                    self.running = False
            elif self.state == GameState.Play:
                if not self.gamePaused:
                    self.playerInput.update(dt)
                self.playUI.update(dt)
                if self.playUI.gameOverReplayPressed:
                    self.reset()
                elif self.playUI.gameOverExitPressed:
                    self.running = False

            self.screen.fill(CLEAR_COLOR)

            if self.state == GameState.Menu:
                self.menu.draw(self.screen)
            elif self.state == GameState.Play:
                self.grid.draw(self.screen)
                self.tetromino.draw(self.screen)

                ##
                # All the UI panels
                infoPosX = self.grid.pixelWidth + self.grid.x + 10
                score = self.font.render(
                    "Score: " + str(self.playerScore),
                    True,
                    (255, 255, 255, 255)
                )
                self.screen.blit(
                    score,
                    (infoPosX, 100)
                )
                score = self.font.render(
                    "Level: " + str(self.playerLevel),
                    True,
                    (255, 255, 255, 255)
                )
                self.screen.blit(
                    score,
                    (infoPosX, 120)
                )

                nextTetromino = KIND_TO_ARRAY[self.tetromino.nextKind]
                cellSize = self.grid.cellPixelSize
                for y in range(4):
                    for x in range(4):
                        if nextTetromino[y*4+x] == 1:
                            tx = infoPosX + x * cellSize
                            ty = infoPosX + y * cellSize

                            pygame.draw.rect(
                                self.screen,
                                VALUE_TO_COLOR[self.tetromino.nextKind+1],
                                pygame.Rect(
                                    tx, ty,
                                    self.grid.blockPixelSize,
                                    self.grid.blockPixelSize,
                                )
                            )
                self.playUI.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


g = Game()
g.run()
pygame.quit()
exit()
