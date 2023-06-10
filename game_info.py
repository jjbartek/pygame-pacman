from utils.image_utils import ImageUtils


class GameInfo:
    DEFAULT_LIVES_START = (2.5, 34.5)
    ICON_LIVE_SIZE_IN_CELLS = 2
    LIVE_ICON = "pacman-open-left"

    def __init__(self, state):
        self.state = state

    def render(self):
        self._render_lives()

    def _render_lives(self):
        x, y = self.DEFAULT_LIVES_START
        for i in range(self.state.pacman.lives-1):
            position = self.state.level.get_cell_position((x, y))
            image = ImageUtils.get(self.LIVE_ICON)
            self.state.screen.blit(image, image.get_rect(center=position))
            x += self.ICON_LIVE_SIZE_IN_CELLS
