from cell_map import CellMap
from game_states import GameStates
from utils.file_utils import FileUtils
from utils.text_utils import TextUtils


class GameInfo:
    DEFAULT_LIVES_START = (2.5, 34.5)
    ICON_LIVE_SIZE_IN_CELLS = 2
    LIVE_ICON = "pacman-open-left"
    MIDDLE_TEXT_SIZE = 20
    MIDDLE_TEXT_CENTER = (13.5, 20)
    START_TEXT_COLOR = (255, 255, 0)
    END_TEXT_COLOR = (255, 0, 0)
    START_TEXT = "READY!"
    END_TEXT = "GAME  OVER"

    def __init__(self, game):
        self.game = game
        self.start_text = TextUtils.get_text(self.START_TEXT, self.MIDDLE_TEXT_SIZE, self.START_TEXT_COLOR)
        self.end_text = TextUtils.get_text(self.END_TEXT, self.MIDDLE_TEXT_SIZE, self.END_TEXT_COLOR)

    def render(self, screen):
        self._render_lives(screen)
        self._render_text(screen)

    def _render_text(self, screen):
        text_to_render = None
        if self.game.state == GameStates.GAME_START:
            text_to_render = self.start_text
        elif self.game.state == GameStates.DEAD_END:
            text_to_render = self.end_text

        if text_to_render is not None:
            position = CellMap.get_cell_position(self.MIDDLE_TEXT_CENTER)
            screen.blit(text_to_render, text_to_render.get_rect(center=position))

    def _render_lives(self, screen):
        x, y = self.DEFAULT_LIVES_START
        for i in range(self.game.pacman.lives - 1):
            position = CellMap.get_cell_position((x, y))
            image = FileUtils.get_image(self.LIVE_ICON)
            screen.blit(image, image.get_rect(center=position))
            x += self.ICON_LIVE_SIZE_IN_CELLS
