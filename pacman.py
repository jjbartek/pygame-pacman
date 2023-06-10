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
    DEFAULT_PACMAN_MOVE_TIME = 140  # milliseconds per cell movement
    ICON_UPDATE_TIME = 100  # milliseconds after icon is updated

    def __init__(self):
        super().__init__()

        self._next_direction = None
        self._icon_counter = 0

    def initialize(self, state):
        self.state = state
        self.image = ImageUtils.get(self.DEFAULT_IMAGE)
        self.direction = self.DEFAULT_DIRECTION
        self._speed = self.DEFAULT_PACMAN_MOVE_TIME

        self.cell = self.state.level.pacman_start_cell
        self._update_position(self.state.level.get_cell_position(self.cell))
        self._last_icon_update = time.time()

    def update(self):
        self._update_direction()
        self._update_icon()
        self._move()

    def _update_direction(self):
        keys_pressed = pygame.key.get_pressed()
        for key in self.KEY_TO_DIRECTION_MAPPING.keys():
            if keys_pressed[key]:
                new_direction = self.KEY_TO_DIRECTION_MAPPING[key]
                self._next_direction = new_direction
                break

        if self._next_direction and self._can_move_at_direction(self._next_direction) and not self._moving:
            self.direction = self._next_direction
            self._next_direction = None

    def _update_icon(self):
        if self._time_elapsed_since_icon_update() >= self.ICON_UPDATE_TIME:
            self.image = ImageUtils.get(self._get_icon_name())
            self._update_counter()
            self._last_icon_update = time.time()

    def _can_move_at_direction(self, direction):
        current_cell = self._target_cell if self._target_cell else self.cell
        next_cell = self._get_next_cell(current_cell, direction)
        return self._is_cell_walkable(next_cell)

    def _time_elapsed_since_icon_update(self):
        return time.time() * 1000 - self._last_icon_update * 1000

    def _get_icon_name(self):
        icon_type = Pacman.ICON_SUFFIX[self._icon_counter]
        direction_in_lowercase = self.direction.name.lower()

        return f"pacman-{icon_type}-{direction_in_lowercase}"

    def _update_counter(self):
        self._icon_counter = (self._icon_counter + 1) % 2

    def _move(self):
        if self._moving:
            self._slow_movement(self._speed)
        else:
            current_cell = self._target_cell if self._target_cell else self.cell
            next_cell = self._get_next_cell(current_cell, self.direction)
            if self._is_cell_walkable(next_cell):
                self._active = True
                self._moving = True
                self._target_cell = next_cell
                self._move_start_time = time.time()
                self._slow_movement(self._speed)

    @classmethod
    def load_icons(cls):
        if not cls._icons_loaded:
            for icon in cls.ICONS_LIST:
                ImageUtils.get(icon)
