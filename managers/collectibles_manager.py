import pygame


class CollectiblesManager:
    def __init__(self):
        self.group = None
        self.state = None

    def initialize(self, state):
        self.group = pygame.sprite.Group()
        self.state = state

    def render(self):
        self.group.draw(self.state.screen)

    def add(self, collectible):
        self.group.add(collectible)

    def update(self):
        for collectible in self.group:
            collision = pygame.sprite.collide_rect(collectible, self.state.pacman)
            if collision:
                collectible.collect(self.state)
            else:
                collectible.update()