import pygame
import os
from collectibles.collectible import Collectible


class Cherry(Collectible):
    ICON_NAME = "cherry"
    POINTS = 100

    def __init__(self, position):
        super().__init__(Cherry.ICON_NAME, position, Cherry.POINTS)

