import time

from cell_map import CellMap
from entities.entity import Entity
from enums.direction import Direction
from enums.ghost_mode import GhostMode
from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


class Pacman(Entity):
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
    DEFAULT_IMAGE = "pacman-open-left"
    DEFAULT_DIRECTION = Direction.LEFT
    START_CELL = (13.5, 26)
    ICON_UPDATE_TIME = 100  # milliseconds after icon is updated
    DEFAULT_LIVES = 3

    def __init__(self, game):
        super().__init__()
        self._load_icons()

        self._next_direction = None
        self._icon_counter = 0
        self.lives = self.DEFAULT_LIVES
        self.is_eating = False
        self.game = game

        self.reset()

    def reset(self):
        super().reset()
        self.image = FileUtils.get_image(self.DEFAULT_IMAGE)
        self.direction = self.DEFAULT_DIRECTION

        self.cell = self.START_CELL
        self._update_position(CellMap.get_cell_position(self.cell))
        self._last_icon_update = time.time()

    def update(self, key_pressed):
        self._update_direction(key_pressed)
        self._update_icon()
        self._move()

    def _update_direction(self, key_pressed):
        for key in self.KEY_TO_DIRECTION_MAPPING.keys():
            if key_pressed[key]:
                new_direction = self.KEY_TO_DIRECTION_MAPPING[key]
                self._next_direction = new_direction
                break

        if self._next_direction and self._can_move_at_direction(self._next_direction) and not self._moving:
            self.direction = self._next_direction
            self._next_direction = None

    def _update_icon(self):
        if TimeUtils.elapsed(self._last_icon_update) >= self.ICON_UPDATE_TIME:
            self.image = FileUtils.get_image(self._get_icon_name())
            self._update_counter()
            self._last_icon_update = time.time()

    def _can_move_at_direction(self, direction):
        current_cell = self._target_cell if self._target_cell else self.cell
        next_cell = CellMap.get_instance().get_next_cell(current_cell, direction)
        return self.is_cell_walkable(next_cell)

    def _get_icon_name(self):
        icon_type = Pacman.ICON_SUFFIX[self._icon_counter]
        direction_in_lowercase = self.direction.name.lower()

        return f"pacman-{icon_type}-{direction_in_lowercase}"

    def _update_counter(self):
        self._icon_counter = (self._icon_counter + 1) % 2

    def _prepare_move(self, speed):
        self.game.collectibles.handle_collision(self.cell)

        next_cell = CellMap.get_instance().get_next_cell(self.cell, self.direction)
        if self.is_cell_walkable(next_cell):
            self._moving = True
            self._target_cell = next_cell
            self._move_start_time = time.time()
            self._animated_movement(speed)

    def _get_speed(self):
        if self.game.ghosts.current_mode == GhostMode.FRIGHTENED:
            if self.is_eating:
                speed_percent = self.game.levels.current.pacman_dots_fright
            else:
                speed_percent = self.game.levels.current.pacman_speed_fright
        else:
            if self.is_eating:
                speed_percent = self.game.levels.current.pacman_dots_normal
            else:
                speed_percent = self.game.levels.current.pacman_speed_normal

        return self._get_speed_by_percent(speed_percent)

    @classmethod
    def _load_icons(cls):
        if not cls._icons_loaded:
            for icon in cls.ICONS_LIST:
                FileUtils.get_image(icon)
