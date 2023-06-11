import time
from abc import ABC, abstractmethod

import pygame

from cell import Cell
from cell_map import CellMap
from direction import Direction


class MovableEntity(pygame.sprite.Sprite, ABC):
    KEY_TO_DIRECTION_MAPPING = {
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN
    }

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        self._active = False
        self._moving = False
        self._move_start_time = None
        self._last_icon_update = None
        self._target_cell = None

    @abstractmethod
    def _move(self):
        pass

    def _slow_movement(self, speed):
        time_elapsed = self._time_elapsed_since_move_start()
        if time_elapsed <= speed:
            position = self._get_transition_position(time_elapsed, speed)
            self._update_position(position)
        else:
            end_position = CellMap.get_cell_position(self._target_cell)
            self._update_position(end_position)
            self.cell = self._target_cell
            self._target_cell = None
            self._moving = False

    def _update_position(self, position):
        self.rect = self.image.get_rect(center=position)

    def _get_transition_position(self, time_elapsed, speed):
        progress = min(round(time_elapsed / speed * 100), 100)
        distance = self._get_distance_covered(progress)
        cell_type = CellMap.get_instance().get_cell_type(self.cell)

        if cell_type == Cell.TUNNEL:
            if progress < 50:
                return self._calculate_regular_position(distance)
            else:
                return self._calculate_tunnel_exit_position(distance)
        else:
            return self._calculate_regular_position(distance)

    def _calculate_regular_position(self, distance):
        direction = self.direction
        x, y = CellMap.get_cell_position(self.cell)

        if direction == Direction.UP:
            y -= distance
        elif direction == Direction.DOWN:
            y += distance
        elif direction == Direction.LEFT:
            x -= distance
        elif direction == Direction.RIGHT:
            x += distance

        return x, y

    def _calculate_tunnel_exit_position(self, distance):
        direction = self.direction
        cell_size = CellMap.CELL_SIZE_IN_PIXELS
        x, y = CellMap.get_cell_position(self._target_cell)

        if direction == Direction.UP:
            y = y + cell_size - distance
        elif direction == Direction.DOWN:
            y = y - cell_size + distance
        elif direction == Direction.LEFT:
            x = x + cell_size - distance
        elif direction == Direction.RIGHT:
            x = x - cell_size + distance

        return x, y

    def _get_distance_covered(self, progress):
        cell_size = CellMap.CELL_SIZE_IN_PIXELS
        cell_type = CellMap.get_instance().get_cell_type(self.cell)
        if cell_type == Cell.TUNNEL:
            return cell_size * progress / 100
        else:
            x, y = self.cell
            target_x, target_y = self._target_cell

            if self.direction == Direction.LEFT or self.direction == Direction.RIGHT:
                full_distance = abs(x - target_x) * cell_size
            else:
                full_distance = abs(y - target_y) * cell_size

            return full_distance * progress / 100

    def _time_elapsed_since_move_start(self):
        return time.time() * 1000 - self._move_start_time * 1000
