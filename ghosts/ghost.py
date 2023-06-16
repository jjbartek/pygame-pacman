import math
import time
from abc import ABC, abstractmethod

import pygame

from cell import Cell
from cell_map import CellMap
from direction import Direction
from game_states import GameStates
from ghosts.ghost_modes import GhostModes
from movable_entity import MovableEntity
from utils.file_utils import FileUtils


class Ghost(MovableEntity, ABC):
    DEFAULT_GHOST_MOVE_TIME = 160
    DEFAULT_DIRECTION = Direction.UP
    FIRST_CELL = (13, 14)
    COLLISION_OFFSET = 5

    NO_MOVE_UP_CELLS = [
        (12, 14), (15, 14), (12, 26), (15, 26)
    ]
    SLOW_CELLS = [
        (0, 17), (1, 17), (2, 17), (3, 17), (4, 17), (5, 17),
        (22, 17), (23, 17), (24, 17), (25, 17), (26, 17), (27, 17)
    ]
    # lowest value - highest priority
    DIRECTION_PRIORITY = {
        Direction.UP: 0,
        Direction.LEFT: 1,
        Direction.DOWN: 2,
        Direction.RIGHT: 3
    }
    REVERSE = {
        Direction.UP: Direction.DOWN,
        Direction.LEFT: Direction.RIGHT,
        Direction.DOWN: Direction.UP,
        Direction.RIGHT: Direction.LEFT
    }

    def __init__(self, name, start_cell, start_real_cell, scatter_cell, color, manager):
        super().__init__()
        self.name = name
        self.start_cell = start_cell
        self.start_real_cell = start_real_cell
        self.manager = manager
        self.color = color
        self.scatter_cell = scatter_cell
        self.cell = self.start_cell
        self.image = FileUtils.get_image(self._get_icon_name())
        self.direction = None
        self.goal_cell = None
        self._speed = self.DEFAULT_GHOST_MOVE_TIME
        self._next_cell = None
        self._next_direction = None
        self._reverse_direction = False
        self._previous_cell = None
        self._out_of_home = False

        self._update_position(CellMap.get_cell_position(self.cell))

    def update(self):
        if self._active:
            self._move()
            self.image = FileUtils.get_image(self._get_icon_name())
            self._detect_collision()

    def reverse_direction(self):
        self._reverse_direction = True

    def _get_goal_cell(self):
        if not self._out_of_home:
            goal = self._get_home_goal_cell()
        elif self.manager.mode == GhostModes.CHASE:
            goal = self.get_chase_cell()
        elif self.manager.mode == GhostModes.SCATTER:
            goal = self.scatter_cell
        else:
            goal = None

        return goal

    def _get_home_goal_cell(self):
        if self.cell == self.FIRST_CELL:
            self._out_of_home = True
            self.direction = Direction.LEFT
            goal = self._get_goal_cell()
        else:
            goal = self.FIRST_CELL

        return goal

    @abstractmethod
    def get_chase_cell(self):
        pass

    def reset(self):
        super().reset()
        self.cell = self.start_cell
        self.direction = None
        self.image = FileUtils.get_image(self._get_icon_name())
        self.goal_cell = None
        self.cell = self.start_cell
        self._speed = self.DEFAULT_GHOST_MOVE_TIME
        self._next_cell = None
        self._next_direction = None
        self._previous_cell = None
        self._reverse_direction = False
        self._active = False
        self._out_of_home = False

        self._update_position(CellMap.get_cell_position(self.cell))

    def _detect_collision(self):
        if self._collides(self.manager.game.pacman.rect.center):
            if self.manager.game.pacman.lives > 1:
                self.manager.game.update_state(GameStates.DEAD)
            else:
                self.manager.game.update_state(GameStates.DEAD_END)

    def _collides(self, center):
        self_x, self_y = self.rect.center
        center_x, center_y = center

        return center_x - self.COLLISION_OFFSET <= self_x <= center_x + self.COLLISION_OFFSET \
            and center_y - self.COLLISION_OFFSET <= self_y <= center_y + self.COLLISION_OFFSET

    def _move(self):
        speed = self._speed
        if self._target_cell and self._target_cell in self.SLOW_CELLS:
            speed *= 1.5

        if self._moving:
            self._slow_movement(speed)
        else:
            self._prepare_move(speed)

    def _prepare_move(self, speed):
        self.goal_cell = self._get_goal_cell()
        if self.direction is None:
            self.direction = self._get_direction_to_cell(self.start_real_cell)
            self._target_cell = self.start_real_cell
        else:
            self._handle_reverse_direction()
            self.direction = self._next_direction
            self._target_cell = self._next_cell

        self._move_start_time = time.time()
        self._moving = True
        possible_moves = self._get_possible_moves(self._target_cell)
        self._next_direction, self._next_cell = self._get_closest_move(possible_moves)
        self._slow_movement(speed)

    def _handle_reverse_direction(self):
        if self._reverse_direction and self._previous_cell is not None:
            self._next_direction = self.REVERSE[self.direction]
            self._next_cell = self._previous_cell
            self._reverse_direction = False

    def _get_direction_to_cell(self, cell):
        x, y = cell
        current_x, current_y = self.cell

        if x < current_x:
            direction = Direction.LEFT
        elif x > current_x:
            direction = Direction.RIGHT
        elif y < current_y:
            direction = Direction.DOWN
        elif y > current_x:
            direction = Direction.UP
        else:
            raise ValueError("Cell must differ from current cell")

        return direction

    def _slow_movement(self, speed):
        time_elapsed = self._time_elapsed_since_move_start()
        if time_elapsed <= speed:
            position = self._get_transition_position(time_elapsed, speed)
            self._update_position(position)
        else:
            end_position = CellMap.get_cell_position(self._target_cell)
            self._update_position(end_position)
            self._previous_cell = self.cell
            self.cell = self._target_cell
            self._target_cell = None
            self._moving = False

    def activate(self):
        self._active = True

    def _get_closest_move(self, moves):
        return min(moves.items(), key=lambda move: self._get_sort_key(move))

    def _get_sort_key(self, item):
        direction, cell = item
        return self._get_distance_to_goal(cell), self.DIRECTION_PRIORITY[direction]

    def _get_distance_to_goal(self, cell):
        x, y = cell
        goal_x, goal_y = self.goal_cell
        return math.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)

    def _get_possible_moves(self, cell):
        moves = {}
        for direction in Direction:
            next_cell = CellMap.get_instance().get_next_cell(cell, direction)
            if self._can_move_to_cell(direction, next_cell):
                moves[direction] = next_cell

        return moves

    def _can_move_to_cell(self, direction, next_cell):
        return (self.direction and direction != self.REVERSE[self.direction]) \
            and self.is_cell_walkable(next_cell) \
            and not (direction == Direction.UP and self._next_cell in self.NO_MOVE_UP_CELLS)

    def _get_icon_name(self):
        direction = self.direction if self.direction else self.DEFAULT_DIRECTION
        direction_in_lowercase = direction.name.lower()

        return f"ghost-{self.name}-{direction_in_lowercase}"

    def is_cell_walkable(self, cell):
        if not CellMap.get_instance().cell_exists(cell):
            return False

        cell_type = CellMap.get_instance().get_cell_type(cell)

        if self._out_of_home:
            return cell_type in [Cell.SPACE, Cell.TUNNEL]
        else:
            return cell_type in [Cell.SPACE, Cell.TUNNEL, Cell.SPACE_GATE]

    def render(self, screen):
        super().render(screen)
        if self._active and self.goal_cell is not None:
            x, y = CellMap.get_cell_position(self.goal_cell, center=False)
            size = CellMap.CELL_SIZE_IN_PIXELS
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, size, size), 2)