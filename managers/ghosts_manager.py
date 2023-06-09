import pygame

from ghosts.inky import Inky
from ghosts.blinky import Blinky
from ghosts.clyde import Clyde
from ghosts.pinky import Pinky


class GhostsManager:
    def __init__(self):
        self.group = None
        self.state = None
        self.blinky = None
        self.pinky = None
        self.inky = None
        self.clyde = None

    def initialize(self, state):
        self.group = pygame.sprite.Group()
        self.state = state

        self.blinky = Blinky(state)
        self.pinky = Pinky(state)
        self.inky = Inky(state)
        self.clyde = Clyde(state)

        self.group.add(self.blinky)
        self.group.add(self.pinky)
        self.group.add(self.inky)
        self.group.add(self.clyde)

        self.blinky.activate()

    def update(self):
        for ghost in self.group:
            ghost.update()

    def render(self):
        self.group.draw(self.state.screen)
