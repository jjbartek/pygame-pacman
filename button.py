import time

import pygame.sprite

from utils.audio_utils import AudioUtils
from utils.file_utils import FileUtils
from utils.text_utils import TextUtils
from utils.time_utils import TimeUtils


class Button(pygame.sprite.Sprite):
    BUTTON_IMAGE = "button"
    BUTTON_HOVER_IMAGE = "button-hover"
    BUTTON_TEXT_SIZE = 25
    BUTTON_TEXT_COLOR = (255, 255, 255)
    BUTTON_CHECK_TIME = 200

    def __init__(self, name, position, on_click):
        super().__init__()
        self.name = name
        self.position = position
        self.image = FileUtils.get_image(self.BUTTON_IMAGE)
        self.hover_image = FileUtils.get_image(self.BUTTON_HOVER_IMAGE)
        self.text = TextUtils.get_standard_text(name, self.BUTTON_TEXT_SIZE, self.BUTTON_TEXT_COLOR)
        self._current_image = self.image
        self.rect = self._current_image.get_rect(center=self.position)
        self._on_click = on_click
        self._timer = time.time()

    def update(self, events):
        mouse_position = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(mouse_position):
                AudioUtils.get_sound(AudioUtils.BUTTON_SOUND).play()
                self._on_click()

        if TimeUtils.elapsed(self._timer) >= self.BUTTON_CHECK_TIME:
            if self.rect.collidepoint(mouse_position):
                self._current_image = self.hover_image
            else:
                self._current_image = self.image

            self.rect = self._current_image.get_rect(center=self.position)
            self._timer = time.time()

    def render(self, screen):
        text_position = (self.position[0], self.position[1] - 2)
        screen.blit(self._current_image, self.rect)
        screen.blit(self.text, self.text.get_rect(center=text_position))
