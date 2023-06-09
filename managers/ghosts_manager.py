import pygame

from ghosts.Inky import Inky
from ghosts.blinky import Blinky
from ghosts.clyde import Clyde
from ghosts.pinky import Pinky


class GhostsManager:
    def __init__(self):
        self.group = None
        self.state = None

    def initialize(self, state):
        self.group = pygame.sprite.Group()
        self.state = state

        self.group.add(Blinky(state))
        self.group.add(Pinky(state))
        self.group.add(Inky(state))
        self.group.add(Clyde(state))

    def update(self):
        for ghost in self.group:
            ghost.update()

    def render(self):
        self.group.draw(self.state.screen)
