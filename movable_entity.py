import time

import pygame
import numbers

from cell import Cell
from direction import Direction


class MovableEntity(pygame.sprite.Sprite):
    POSITION_MAPPING = {
        Direction.UP.value: (0, -1),
        Direction.DOWN.value: (0, 1),
        Direction.RIGHT.value: (1, 0),
        Direction.LEFT.value: (-1, 0),
    }

    KEY_TO_DIRECTION_MAPPING = {
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN
    }

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.state = None
        self.image = None
        self.cell = None
        self.rect = None
        self.direction = None
        self._active = False
        self._speed = 0
        self._moving = False
        self._move_start_time = None
        self._last_icon_update = None
        self._target_cell = None

    def render(self):
        self.state.screen.blit(self.image, self.rect)

    def _move(self):
        pass

    def _slow_movement(self):
        time_elapsed = self._time_elapsed_since_move_start()
        if time_elapsed <= self._speed:
            position = self._get_distance_covered(time_elapsed)
            self._update_position(position)
        else:
            end_position = self.state.level.get_cell_position(self._target_cell)
            self._update_position(end_position)
            self.cell = self._target_cell
            self._target_cell = None
            self._moving = False

    def _update_position(self, position):
        self.rect = self.image.get_rect(center=position)

    def _get_distance_covered(self, time_elapsed):
        start_x, start_y = self.state.level.get_cell_position(self.cell)
        end_x, end_y = self.state.level.get_cell_position(self._target_cell)
        progress = round((time_elapsed / self._speed) * 100)

        if progress == 0:
            return start_x, start_y
        elif progress > 100:
            return end_x, end_x

        distance_x, distance_y = (abs((end_x - start_x) * progress / 100), abs((end_y - start_y) * progress / 100))

        if start_x > end_x:
            result_x = start_x - distance_x
        else:
            result_x = start_x + distance_x

        if start_y > end_y:
            result_y = start_y - distance_y
        else:
            result_y = start_y + distance_y

        return result_x, result_y

    def _time_elapsed_since_move_start(self):
        return time.time() * 1000 - self._move_start_time * 1000

    def _get_next_cell(self, direction):
        if self._active is False:
            self._convert_cell_to_integers()
        current_cell = self._target_cell if self._target_cell else self.cell
        next_cell = tuple(map(sum, zip(current_cell, self.POSITION_MAPPING.get(direction.value))))
        if self._get_cell_type(self.cell) is Cell.TUNNEL and not self._cell_exists(next_cell):
            x_cells, y_cells = self.state.level.cells_per_plane
            x, y = next_cell
            next_cell = x % x_cells, y % y_cells
        return next_cell

    def _convert_cell_to_integers(self):
        # this is necessary for starting cell - which may be a float
        x, y = self.cell
        self.cell = int(x), int(y)

    def _can_move_at_direction(self, direction):
        next_cell = self._get_next_cell(direction)
        return self._can_move_to_cell(next_cell)

    def _can_move_to_cell(self, cell):
        return self._cell_exists(cell) and self._is_cell_walkable(cell)

    def _cell_exists(self, cell):
        x, y = cell
        x_cells, y_cells = self.state.level.cells_per_plane
        return 0 <= x <= x_cells - 1 and 0 <= y <= y_cells - 1

    def _is_cell_walkable(self, cell):
        cell_type = self._get_cell_type(cell)
        return cell_type is Cell.SPACE or cell_type is Cell.TUNNEL

    def _get_cell_type(self, cell):
        x, y = cell
        return self.state.level.map[y][x]
