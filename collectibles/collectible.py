import pygame

from utils.image_utils import ImageUtils


class Collectible(pygame.sprite.Sprite):
    images = {}

    def __init__(self, image, position, score):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.get_image(image)
        self.position = position
        self.score = score
        self.rect = self.image.get_rect(center=position)

    def when_collected(self):
        pass

    @classmethod
    def get_image(cls, name):
        if name not in cls.images:
            cls.images[name] = ImageUtils.get(name)

        return cls.images[name]