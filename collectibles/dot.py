from collectibles.collectible import Collectible
from utils.image_utils import ImageUtils


class Dot(Collectible):
    ICON_NAME = "small-point"
    POINTS = 10

    def __init__(self, position, cell):
        super().__init__(ImageUtils.get(self.ICON_NAME), position, Dot.POINTS, cell)
        self._icon_counter = 0