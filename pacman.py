import time

import pygame

from direction import Direction
from movable_entity import MovableEntity
from utils.image_utils import ImageUtils


class Pacman(MovableEntity):
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
        super().__init__()

        self._last_pacman_update = None
        self._icon_counter = 0

    def initialize(self, state):
        self.state = state
        self.image = Pacman.icons.get(self.DEFAULT_IMAGE)
        self.direction = self.DEFAULT_DIRECTION

        self.cell = self.state.level.default_cell
        self.rect = self.image.get_rect(center=self.state.level.get_cell_position(self.cell))
        self._last_pacman_update = time.time()

    def update(self):
        self._update_direction()
        self._update_icon()
        self._move()

    def _update_direction(self):
        keys_pressed = pygame.key.get_pressed()
        for key in self.KEY_TO_DIRECTION_MAPPING.keys():
            if keys_pressed[key]:
                new_direction = self.KEY_TO_DIRECTION_MAPPING[key]
                if self._can_move_at_direction(new_direction):
                    self.direction = new_direction
                break

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
        next_cell = self._get_next_cell(self.direction)
        if self._can_move_to_cell(next_cell):
            self._active = True
            self.cell = next_cell
            self._update_icon_position()

    def _update_icon_position(self):
        self.rect = self.image.get_rect(center=self.state.level.get_cell_position(self.cell))

    @classmethod
    def load_icons(cls):
        if cls._icons_loaded is False:
            for icon in cls.ICONS_LIST:
                cls.icons[icon] = ImageUtils.get(icon)
