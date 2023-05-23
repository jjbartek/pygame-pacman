import pygame
import os
from elements.element import Element


class Dot(Element):
    icon = pygame.image.load(os.path.join('resources', 'images', 'small-point.png'))

    def __init__(self, position):
        super().__init__(Dot.icon, position, 1000)
