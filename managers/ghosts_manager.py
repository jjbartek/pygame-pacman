import pygame

from ghosts.inky import Inky
from ghosts.blinky import Blinky
from ghosts.clyde import Clyde
from ghosts.pinky import Pinky


class GhostsManager:
    def __init__(self, game):
        self.game = game
        self.group = pygame.sprite.Group()
        self.blinky = Blinky(self.game)
        self.pinky = Pinky(self.game)
        self.inky = Inky(self.game)
        self.clyde = Clyde(self.game)

        self.group.add(self.blinky)
        self.group.add(self.pinky)
        self.group.add(self.inky)
        self.group.add(self.clyde)

        self.blinky.activate()

    def update(self):
        for ghost in self.group:
            ghost.update()

    def render(self, screen):
        self.group.draw(screen)

    def reset(self):
        for ghost in self.group:
            ghost.reset()

        self.blinky.activate()
