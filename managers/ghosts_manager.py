import pygame


class GhostsManager:
    def __init__(self):
        self.group = None
        self.state = None

    def initialize(self, state):
        self.group = pygame.sprite.Group()
        self.state = state

    def render(self):
        self.group.draw()

    def add(self, collectible):
        self.group.add(collectible)
