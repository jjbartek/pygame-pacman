from enum import Enum

import pygame

from stages.game_stage import GameStage
from stages.menu_stage import MenuStage
from stages.pause_menu_stage import PauseMenuStage
from stages.stage import Stages
from stages.start_menu_stage import StartMenuStage
from utils.file_utils import FileUtils


class Game:
    MAX_FPS = 60
    GAME_ICON_NAME = "icon"
    GAME_TITLE = "PACMAN"
    DIMENSIONS = (560, 720)

    def __init__(self):
        pygame.init()

        self._clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.DIMENSIONS)
        self.start_menu_stage = StartMenuStage()
        self.pause_menu_stage = PauseMenuStage()
        self.game_stage = GameStage()
        self.current_stage = self.start_menu_stage

        self.start_menu_stage.subscribe(self._update_stage)
        self.pause_menu_stage.subscribe(self._update_stage)
        self.game_stage.subscribe(self._update_stage)

        self._update_window()

    def run(self):
        while self.current_stage:
            self._update()
            self._render()

            self._clock.tick(Game.MAX_FPS)
            pygame.display.update()

        self._terminate()

    def _update_stage(self, new_stage_type):
        if new_stage_type == Stages.GAME:
            if self.current_stage == self.start_menu_stage:
                self.game_stage.start_game()

            self.current_stage = self.game_stage
        elif new_stage_type == Stages.MENU:
            self.current_stage = self.start_menu_stage
        elif new_stage_type == Stages.PAUSE:
            self.current_stage = self.pause_menu_stage
        elif new_stage_type == Stages.QUIT:
            self.current_stage = None

    def _update(self):
        events = pygame.event.get()
        key_pressed = pygame.key.get_pressed()
        if self.current_stage:
            self.current_stage.update(events, key_pressed)
        self._handle_events(events, key_pressed)

    def _render(self):
        if self.current_stage:
            self.current_stage.render(self.screen)

    def _handle_events(self, events, key_pressed):
        if key_pressed[pygame.K_ESCAPE]:
            self._quit()

        for event in events:
            if event.type == pygame.QUIT:
                self._quit()

    def _quit(self):
        if self.current_stage == self.game_stage:
            self._update_stage(Stages.PAUSE)
        else:
            self._update_stage(Stages.QUIT)
        pygame.time.wait(500)

    def _update_window(self):
        icon = FileUtils.get_image(self.GAME_ICON_NAME)

        pygame.display.set_caption(self.GAME_TITLE)
        pygame.display.set_icon(icon)
        pygame.display.flip()

    @staticmethod
    def _terminate():
        pygame.quit()
