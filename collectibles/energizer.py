import pygame
import os
from collectibles.collectible import Collectible


class Energizer(Collectible):
    ICON_NAME = "big-point"
    POINTS = 50

    def __init__(self, position):
        super().__init__(Energizer.ICON_NAME, position, Energizer.POINTS)
