import time

from collectibles.collectible import Collectible
from utils.image_utils import ImageUtils
from utils.time_utils import TimeUtils


class Energizer(Collectible):
    ICON_NAME = "big-point"
    POINTS = 50
    ALL_ICONS = ["big-point", "big-point-empty"]
    UPDATE_TIME = 200

    def __init__(self, position, cell):
        super().__init__(ImageUtils.get(self.ICON_NAME), position, Energizer.POINTS, cell)
        self._icon_counter = 0
        self._last_icon_update = time.time()

    def update(self):
        if TimeUtils.time_elapsed_since(self._last_icon_update) >= self.UPDATE_TIME:
            self.image = self._get_next_icon()
            self._last_icon_update = time.time()

    def _get_next_icon(self):
        self._icon_counter = (self._icon_counter + 1) % len(self.ALL_ICONS)
        return ImageUtils.get(self.ALL_ICONS[self._icon_counter])
