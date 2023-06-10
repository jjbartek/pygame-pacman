import pygame

from utils.image_utils import ImageUtils


class Collectible(pygame.sprite.Sprite):
    def __init__(self, image, position, score):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.position = position
        self.score = score
        self.rect = self.image.get_rect(center=position)

    def collect(self, state):
        state.add_score(self.score)
        self.kill()

    def update(self):
        pass