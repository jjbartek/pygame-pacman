import pygame


class Dot(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 10))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=center_pos)