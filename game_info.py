from cell_map import CellMap
from game_states import GameStates
from utils.file_utils import FileUtils
from utils.text_utils import TextUtils


class GameInfo:
    LIVE_ICON = "pacman-open-left"
    DEFAULT_LIVES_START = (2.5, 34.5)
    SCORE_TITLE_POS = (4, 0.5)
    SCORE_POS = (4, 1.5)
    HIGH_SCORE_POS = (13.5, 1.5)
    HIGH_SCORE_TITLE_POS = (14, 0.5)
    MIDDLE_TEXT_CENTER = (13.5, 20)
    ICON_LIVE_SIZE_IN_CELLS = 2
    MIDDLE_TEXT_SIZE = 20
    TOP_TEXT_SIZE = 18
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    START_TEXT = "READY!"
    END_TEXT = "GAME  OVER"
    SCORE_TITLE = "1UP"
    HIGH_SCORE_TEXT = "HIGH SCORE"

    def __init__(self, game):
        self.game = game
        self.start_text = TextUtils.get_text(self.START_TEXT, self.MIDDLE_TEXT_SIZE, self.YELLOW)
        self.end_text = TextUtils.get_text(self.END_TEXT, self.MIDDLE_TEXT_SIZE, self.RED)
        self.score_title = TextUtils.get_text(self.SCORE_TITLE, self.TOP_TEXT_SIZE, self.WHITE)
        self.high_score_title = TextUtils.get_text(self.HIGH_SCORE_TEXT, self.TOP_TEXT_SIZE, self.WHITE)

    def render(self, screen):
        self._render_lives(screen)
        self._render_text(screen)
        self._render_score(screen)
        self._render_high_score(screen)

    def _render_score(self, screen):
        score_value = TextUtils.get_text(str(self.game.score), self.TOP_TEXT_SIZE, self.WHITE, cache=False)
        title_position = CellMap.get_cell_position(self.SCORE_TITLE_POS)
        score_position = CellMap.get_cell_position(self.SCORE_POS)
        screen.blit(self.score_title, self.score_title.get_rect(center=title_position))
        screen.blit(score_value, score_value.get_rect(center=score_position))

    def _render_high_score(self, screen):
        highest_score = max(self.game.score, self.game.high_score)
        score_value = TextUtils.get_text(str(highest_score), self.TOP_TEXT_SIZE, self.WHITE, cache=False)
        title_position = CellMap.get_cell_position(self.HIGH_SCORE_TITLE_POS)
        score_position = CellMap.get_cell_position(self.HIGH_SCORE_POS)
        screen.blit(self.high_score_title, self.high_score_title.get_rect(center=title_position))
        screen.blit(score_value, score_value.get_rect(center=score_position))

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
