import pygame

TICKRATES = [
    0.8, 0.72, 0.63, 0.55,
    0.47, 0.38, 0.3, 0.22,
    0.13, 0.1, 0.08, 0.07,
    0.05, 0.03, 0.02,
]

SOFT_DROP_FACTOR = 20


class PlayerInput:
    def __init__(self) -> None:
        self.tickTimer: float = 0
        self.tickRateIndex = 0
        self.tickRate: float = TICKRATES[self.tickRateIndex]
        self.inputAvailable = True
        self.inputTimer: float = 0
        self.inputRate: float = 0.2
        self.listeners = []
        self.down = False
        self.previousDown = self.down

    def reset(self):
        self.tickTimer: float = 0
        self.tickRate: float = TICKRATES[self.tickRateIndex]
        self.inputAvailable = True
        self.inputTimer: float = 0
        self.inputRate: float = 0.2
        self.down = False
        self.previousDown = self.down

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.previousDown = self.down
        self.down = keys[pygame.K_s]

        if self.down and not self.previousDown:
            self.tickRate = TICKRATES[self.tickRateIndex] / SOFT_DROP_FACTOR
        elif not self.down and self.previousDown:
            self.tickRate = TICKRATES[self.tickRateIndex]

        self.tickTimer += dt
        if self.tickTimer >= self.tickRate:
            self.tickTimer = 0
            for listener in self.listeners:
                listener.onEvent("tick")

        if self.inputAvailable:
            event = ""
            if keys[pygame.K_a]:
                event = "left"
            elif keys[pygame.K_d]:
                event = "right"
            elif keys[pygame.K_w]:
                event = "rotate"
            if event != "":
                self.inputAvailable = False
                for listener in self.listeners:
                    listener.onEvent(event)
        else:
            # advance the timer
            self.inputTimer += dt
            if self.inputTimer >= self.inputRate:
                self.inputTimer = 0
                self.inputAvailable = True

    def addListener(self, listener):
        self.listeners.append(listener)

    def increaseTickRate(self):
        self.tickRate = TICKRATES[self.tickRateIndex]
