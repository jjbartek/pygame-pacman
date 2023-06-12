from cell_map import CellMap
from utils.file_utils import FileUtils


class GameInfo:
    DEFAULT_LIVES_START = (2.5, 34.5)
    ICON_LIVE_SIZE_IN_CELLS = 2
    LIVE_ICON = "pacman-open-left"

    def __init__(self, game):
        self.game = game

    def render(self, screen):
        self._render_lives(screen)

    def _render_lives(self, screen):
        x, y = self.DEFAULT_LIVES_START
        for i in range(self.game.pacman.lives - 1):
            position = CellMap.get_cell_position((x, y))
            image = FileUtils.get_image(self.LIVE_ICON)
            screen.blit(image, image.get_rect(center=position))
            x += self.ICON_LIVE_SIZE_IN_CELLS
