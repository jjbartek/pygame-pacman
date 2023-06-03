import pygame

from utils.image_utils import ImageUtils
from state import State


class Game:
    MAX_FPS = 8
    GAME_ICON_NAME = "icon"
    GAME_TITLE = "PACMAN"

    def __init__(self):
        self.state = None
        self._clock = None

    def run(self):
        self._initialize()
        while self.state.is_running:
            self._update()
            self._render()

            self._clock.tick(Game.MAX_FPS)
            pygame.display.update()

        self._terminate()

    def _update(self):
        self._handle_quit()
        self.state.pacman.update()

    def _render(self):
        self.state.level.render()
        self.state.collectibles.render()
        self.state.pacman.render()

    def _handle_quit(self):
        events = pygame.event.get()
        for event in events:
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[pygame.K_ESCAPE]:
                self.state.is_running = False

    def _initialize(self):
        pygame.init()

        self._clock = pygame.time.Clock()
        self.state = State()
        self.state.is_running = True

        self._initialize_screen()
        self.state.pacman.load_icons()

        self.state.collectibles.initialize(self.state)
        self.state.level.initialize(self.state)
        self.state.pacman.initialize(self.state)

        pygame.display.flip()

    def _initialize_screen(self):
        dimensions = self.state.level.dimensions_in_pixels
        self.state.screen = pygame.display.set_mode(dimensions)
        icon = ImageUtils.get(self.GAME_ICON_NAME)

        pygame.display.set_caption(self.GAME_TITLE)
        pygame.display.set_icon(icon)

    @staticmethod
    def _terminate():
        pygame.quit()
