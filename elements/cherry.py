import pygame
import os
from elements.element import Element


class Cherry(Element):
    icon = pygame.image.load(os.path.join('resources', 'images', 'cherry.png'))

    def __init__(self, position):
        super().__init__(Cherry.icon, position, 3000)