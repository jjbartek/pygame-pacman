import time

import pygame

from direction import Direction
from utils.direction_utils import DirectionUtils
from utils.image_utils import ImageUtils


class Pacman(pygame.sprite.Sprite):
    _icons_loaded = False
    icons = {}

    ICON_SUFFIX = {
        0: "whole",
        1: "open"
    }
    ICONS_LIST = {
        "pacman-dead", "pacman-half-down", "pacman-half-left", "pacman-half-up", "pacman-half-right",
        "pacman-open-down", "pacman-open-left", "pacman-open-up", "pacman-open-right",
        "pacman-third-down", "pacman-third-left", "pacman-third-up", "pacman-third-right",
        "pacman-whole-down", "pacman-whole-left", "pacman-whole-up", "pacman-whole-right"
    }
    DEFAULT_IMAGE = "pacman-whole-up"
    DEFAULT_DIRECTION = Direction.UP

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.state = None
        self.active = False
        self.image = None
        self.direction = self.DEFAULT_DIRECTION
        self.cell = None
        self.rect = None
        self._last_pacman_update = None
        self._icon_counter = 0

    def initialize(self, state):
        self.state = state
        self.image = Pacman.icons.get(self.DEFAULT_IMAGE)

        self.cell = self.state.level.default_cell
        self.rect = self.image.get_rect(center=self.state.level.get_cell_position(self.cell))
        self._last_pacman_update = time.time()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in DirectionUtils.KEY_TO_DIRECTION_MAPPING:
                self.direction = DirectionUtils.KEY_TO_DIRECTION_MAPPING[event.key]
                self.active = True
                break

        self._update_icon()
        self._move()

    def render(self):
        surface = self.state.level.surface
        surface.blit(self.image, self.rect)

    def _update_icon(self):
        self.image = Pacman.icons.get(self._get_pacman_icon_name())
        self._update_counter()

    def _get_pacman_icon_name(self):
        icon_type = Pacman.ICON_SUFFIX[self._icon_counter]
        direction_in_lowercase = self.direction.name.lower()

        return f"pacman-{icon_type}-{direction_in_lowercase}"

    def _update_counter(self):
        self._icon_counter = (self._icon_counter + 1) % 2

    def _move(self):
        pass

    @classmethod
    def load_icons(cls):
        if cls._icons_loaded is False:
            for icon in cls.ICONS_LIST:
                cls.icons[icon] = ImageUtils.get(icon)
