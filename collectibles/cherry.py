from collectibles.collectible import Collectible
from utils.file_utils import FileUtils


class Cherry(Collectible):
    ICON_NAME = "cherry"
    POINTS = 100

    def __init__(self, position, cell):
        super().__init__(FileUtils.get_image(self.ICON_NAME), position, Cherry.POINTS, cell)

