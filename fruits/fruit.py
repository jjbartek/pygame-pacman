import time

import pygame.sprite

from enums.units import Units
from utils.text_utils import TextUtils
from utils.time_utils import TimeUtils


class Fruit(pygame.sprite.Sprite):
    COLLISION_OFFSET = 15
    KILL_TIME = 10

    def __init__(self, image, position, cell):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.position = position
        self.cell = cell
        self.rect = self.image.get_rect(center=position)
        self.text = None
        self._created = time.time()

    def collides(self, center):
        self_x, self_y = self.rect.center
        center_x, center_y = center

        return center_x - self.COLLISION_OFFSET <= self_x <= center_x + self.COLLISION_OFFSET \
            and center_y - self.COLLISION_OFFSET <= self_y <= center_y + self.COLLISION_OFFSET

    def set_text(self, score):
        self.text = TextUtils.get_score_text(score)

    def update(self):
        if TimeUtils.elapsed(self._created, unit=Units.Seconds) >= self.KILL_TIME:
            self.kill()

    def render(self, screen):
        if self.text is not None:
            screen.blit(self.text, self.text.get_rect(center=self.position))
        else:
            screen.blit(self.image, self.rect)
