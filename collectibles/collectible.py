import pygame

from utils.image_utils import ImageUtils


class Collectible(pygame.sprite.Sprite):
    images = {}

    def __init__(self, image_name, position, score):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.get_image(image_name)
        self.position = position
        self.score = score
        self.rect = self.image.get_rect(center=position)

    def collect(self, state):
        state.add_score(self.score)

    @classmethod
    def get_image(cls, name):
        if name not in cls.images:
            cls.images[name] = ImageUtils.get(name)

        return cls.images[name]