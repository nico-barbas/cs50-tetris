import pygame

pygame.mixer.init()

lineScoreSound = pygame.mixer.Sound("assets/blop.wav")
lineScoreSound.set_volume(0.1)
tetrominoMovedSound = pygame.mixer.Sound("assets/blip.wav")
tetrominoMovedSound.set_volume(0.05)
uiSelectSound = pygame.mixer.Sound("assets/uiSelect.wav")
uiSelectSound.set_volume(0.1)


def playSound(event):
    if event == "lineScored" or event == "uiMove":
        lineScoreSound.play()
    elif event == "tetrominoMoved":
        tetrominoMovedSound.play()
    elif event == "uiSelect":
        uiSelectSound.play()