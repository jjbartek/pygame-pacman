import pygame
import os
from elements.element import Element


class Energizer(Element):
    icon = pygame.image.load(os.path.join('resources', 'images', 'big-point.png'))

    def __init__(self, position):
        super().__init__(Energizer.icon, position, 2000)
