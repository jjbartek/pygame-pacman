from collectibles.collectible import Collectible
from utils.image_utils import ImageUtils


class Cherry(Collectible):
    ICON_NAME = "cherry"
    POINTS = 100

    def __init__(self, position, cell):
        super().__init__(ImageUtils.get(self.ICON_NAME), position, Cherry.POINTS, cell)

