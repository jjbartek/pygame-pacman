import pygame
import os
from collectibles.collectible import Collectible
from utils.image_utils import ImageUtils


class Energizer(Collectible):
    ICON_NAME = "big-point"
    POINTS = 50

    def __init__(self, position):
        super().__init__(ImageUtils.get(self.ICON_NAME), position, Energizer.POINTS)
