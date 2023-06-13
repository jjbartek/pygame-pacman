from collectibles.collectible import Collectible
from utils.file_utils import FileUtils


class Dot(Collectible):
    ICON_NAME = "small-point"
    POINTS = 10

    def __init__(self, position, cell):
        super().__init__(FileUtils.get_image(self.ICON_NAME), position, Dot.POINTS, True, cell)
        self._icon_counter = 0