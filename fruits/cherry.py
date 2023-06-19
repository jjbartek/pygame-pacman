from fruits.fruit import Fruit
from utils.file_utils import FileUtils


class Cherry(Fruit):
    ICON_NAME = "cherry"

    def __init__(self, position, cell):
        super().__init__(FileUtils.get_image(self.ICON_NAME), position, cell)