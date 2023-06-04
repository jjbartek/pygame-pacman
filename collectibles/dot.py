import pygame
import os
from collectibles.collectible import Collectible


class Dot(Collectible):
    ICON_NAME = "small-point"
    POINTS = 10

    def __init__(self, position):
        super().__init__(Dot.ICON_NAME, position, Dot.POINTS)
