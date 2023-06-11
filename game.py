import pygame

from game_info import GameInfo
from utils.file_utils import FileUtils
from board import Board


class Game:
    MAX_FPS = 60
    GAME_ICON_NAME = "icon"
    GAME_TITLE = "PACMAN"
    DIMENSIONS = (560, 720)

    def __init__(self):
        pygame.init()

        self._clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.DIMENSIONS)
        self.is_running = True
        self.board = Board()

        self._initialize_screen()
        self.board.start_game()  # move to update when chosen in menu

    def run(self):
        while self.is_running:
            self._update()
            self._render()

            self._clock.tick(Game.MAX_FPS)
            pygame.display.update()

        self._terminate()

    def _update(self):
        self._handle_quit()
        self.board.update()

    def _render(self):
        self.board.render(self.screen)

    def _handle_quit(self):
        events = pygame.event.get()
        for event in events:
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[pygame.K_ESCAPE]:
                self.is_running = False

    def _initialize_screen(self):
        icon = FileUtils.get_image(self.GAME_ICON_NAME)

        pygame.display.set_caption(self.GAME_TITLE)
        pygame.display.set_icon(icon)
        pygame.display.flip()

    @staticmethod
    def _terminate():
        pygame.quit()
