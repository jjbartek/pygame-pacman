import pygame

from stages.menu_stage import MenuStage
from stages.stage import StageUpdateType


class PauseMenuStage(MenuStage):
    CONTINUE_BUTTON = "CONTINUE"
    RESTART_BUTTON = "RESTART"
    QUIT_BUTTON = "QUIT"

    def __init__(self):
        super().__init__()

    def start_stage(self, update_type):
        pygame.mixer.pause()

    def _add_buttons(self):
        self._add_button(self.CONTINUE_BUTTON, self._continue_clicked)
        self._add_button(self.RESTART_BUTTON, self._restart_clicked)
        self._add_button(self.QUIT_BUTTON, self._quit_clicked)

    def _continue_clicked(self):
        self.notify(StageUpdateType.CONTINUE)

    def _quit_clicked(self):
        self.notify(StageUpdateType.QUIT)

    def _restart_clicked(self):
        self.notify(StageUpdateType.RESTART)

    def update(self, events, key_pressed):
        for event in events:
            if key_pressed[pygame.K_ESCAPE]:
                self.notify(StageUpdateType.CONTINUE)
                return
        super().update(events, key_pressed)
