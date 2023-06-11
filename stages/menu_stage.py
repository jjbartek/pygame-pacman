from abc import ABC, abstractmethod
import pygame.sprite

from button import Button
from stages.stage import Stage
from utils.file_utils import FileUtils


class MenuStage(Stage, ABC):
    BACKGROUND_NAME = "menu"
    BUTTON_SIZE = (334, 69)
    BUTTON_GAP = 40
    FIRST_BUTTON_POSITION = (280, 390)

    def __init__(self):
        super().__init__()
        self.background = FileUtils.get_image(self.BACKGROUND_NAME)
        self.buttons = pygame.sprite.Group()
        self._button_counter = 1

        self._add_buttons()

    @abstractmethod
    def _add_buttons(self):
        pass

    def update(self, events, key_pressed):
        for button in self.buttons:
            button.update(events)

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.render(screen)

    def _add_button(self, text, on_click):
        new_button = Button(text, self._get_button_position(self._button_counter), on_click)

        self.buttons.add(new_button)
        self._button_counter += 1

    def _get_button_position(self, number):
        y = self.FIRST_BUTTON_POSITION[1] + (self.BUTTON_SIZE[1] + self.BUTTON_GAP) * (number - 1)
        return self.FIRST_BUTTON_POSITION[0], y


