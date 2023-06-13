import pygame

from stages.game_stage import GameStage
from stages.pause_menu_stage import PauseMenuStage
from stages.stage import StageUpdateType
from stages.start_menu_stage import StartMenuStage
from utils.audio_utils import AudioUtils
from utils.file_utils import FileUtils


class Game:
    MAX_FPS = 60
    GAME_ICON_NAME = "icon"
    GAME_TITLE = "PACMAN"
    DIMENSIONS = (560, 720)

    def __init__(self):
        pygame.init()
        AudioUtils.load_sounds()

        self._clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.DIMENSIONS)
        self.start_menu_stage = StartMenuStage()
        self.pause_menu_stage = PauseMenuStage()
        self.game_stage = GameStage()
        self.current_stage = self.start_menu_stage

        self.start_menu_stage.subscribe(self._update_stage)
        self.pause_menu_stage.subscribe(self._update_stage)
        self.game_stage.subscribe(self._update_stage)

        self.stage_map = {
            StageUpdateType.START_MENU: self.start_menu_stage,
            StageUpdateType.RESTART: self.game_stage,
            StageUpdateType.CONTINUE: self.game_stage,
            StageUpdateType.PAUSE: self.pause_menu_stage,
            StageUpdateType.QUIT: None,
        }

        self._update_window()

    def run(self):
        while self.current_stage:
            self._update()
            self._render()

            self._clock.tick(Game.MAX_FPS)
            pygame.display.update()
            pygame.event.pump()

        self._terminate()

    def _update_stage(self, update_type):
        pygame.time.wait(300)
        self.current_stage = self.stage_map[update_type]
        if self.current_stage:
            self.current_stage.start_stage(update_type)

    def _update(self):
        events = pygame.event.get()
        key_pressed = pygame.key.get_pressed()
        if self.current_stage:
            self.current_stage.update(events, key_pressed)
        self._handle_events(events)

    def _render(self):
        if self.current_stage:
            self.current_stage.render(self.screen)

    def _handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._update_stage(StageUpdateType.QUIT)
                break

    def _update_window(self):
        icon = FileUtils.get_image(self.GAME_ICON_NAME)

        pygame.display.set_caption(self.GAME_TITLE)
        pygame.display.set_icon(icon)
        pygame.display.flip()

    @staticmethod
    def _terminate():
        pygame.quit()
