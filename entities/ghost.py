import math
import random
import time
from abc import ABC, abstractmethod

import pygame

from enums.cell import Cell
from cell_map import CellMap
from enums.direction import Direction
from enums.game_states import GameState
from enums.ghost_mode import GhostMode
from entities.entity import Entity
from enums.ghost_state import GhostState
from utils.file_utils import FileUtils
from utils.text_utils import TextUtils
from utils.time_utils import TimeUtils


class Ghost(Entity, ABC):
    GHOST_FRIGHT_ICON_TIME = 300
    DEAD_SPEED_PERCENT = 190
    DEFAULT_DIRECTION = Direction.UP
    GHOST_FRIGHT_ICONS = 2
    FIRST_CELL = (13, 14)
    COLLISION_OFFSET = 8

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

    def __init__(self, start_cell, start_real_cell, scatter_cell, color, dots_after_death, manager):
        super().__init__()
        self.start_cell = start_cell
        self.start_real_cell = start_real_cell
        self.dots_after_death = dots_after_death
        self.manager = manager
        self.color = color
        self.scatter_cell = scatter_cell
        self.cell = self.start_cell
        self.state = GhostState.IDLE
        self.image = None
        self.direction = None
        self.goal_cell = None
        self._next_cell = None
        self._next_direction = None
        self._reverse_direction = False
        self._previous_cell = None
        self._already_died = False
        self._icon_counter = 0
        self._last_icon_update = None
        self._dead_text = None

        self.reset()

    def reset(self):
        super().reset()
        self.cell = self.start_cell
        self.direction = None
        self.goal_cell = None
        self.cell = self.start_cell
        self.state = GhostState.IDLE
        self._next_cell = None
        self._next_direction = None
        self._previous_cell = None
        self._reverse_direction = False
        self._already_died = False
        self._icon_counter = 0
        self._last_icon_update = None
        self._dead_text = None
        self.image = FileUtils.get_image(self._get_icon_name())

        self._update_position(CellMap.get_cell_position(self.cell))

    def update(self):
        if self.state == GhostState.DEAD:
            self._dead_text = None

        if self.state != GhostState.IDLE:
            self._move()
            self.image = FileUtils.get_image(self._get_icon_name())
            self._handle_collision()

    def _prepare_move(self, speed):
        self._update_ghost()
        self._handle_reverse_direction()

        self.direction = self._next_direction
        self._target_cell = self._next_cell
        self._move_start_time = time.time()
        self._assign_next_move()
        self._moving = True
        self._animated_movement(speed)

    def _get_speed(self):
        if self.state == GhostState.DEAD:
            speed_percent = self.DEAD_SPEED_PERCENT
        elif self.manager.current_mode == GhostMode.FRIGHTENED and not self._already_died:
            speed_percent = self.manager.game.levels.current.ghost_speed_fright
        elif self._target_cell and self._target_cell in self.SLOW_CELLS:
            speed_percent = self.manager.game.levels.current.ghost_speed_tunnel
        else:
            speed_percent = self.manager.game.levels.current.ghost_speed_normal

        return self._get_speed_by_percent(speed_percent)

    def reverse_direction(self):
        if self.state != GhostState.IDLE or self.state != GhostState.DEAD:
            self._reverse_direction = True

    def reset_dead(self):
        self._already_died = False
        self._last_icon_update = None
        self._icon_counter = 0

    def _update_ghost(self):
        if self.state == GhostState.LEAVING_HOME:
            self._update_leaving_home()
        elif self.state == GhostState.ACTIVE:
            self._update_active()
        elif self.state == GhostState.DEAD:
            self._update_going_home()

    def _update_leaving_home(self):
        if self.direction is None:
            self._next_direction = self._get_direction_to_cell(self.start_real_cell)
            self._next_cell = self.start_real_cell
            self.goal_cell = self.FIRST_CELL
        elif self.cell == self.FIRST_CELL:
            self.state = GhostState.ACTIVE
            self._update_ghost()

    def _update_active(self):
        goal = None
        if self.manager.current_mode == GhostMode.FRIGHTENED and self._already_died:
            mode = self.manager.previous_mode
        else:
            mode = self.manager.current_mode

        if mode == GhostMode.SCATTER:
            goal = self.scatter_cell
        elif mode == GhostMode.CHASE:
            goal = self._get_chase_cell()

        self.goal_cell = goal

    def _update_going_home(self):
        if self.goal_cell != self.start_real_cell:
            self.goal_cell = self.start_real_cell

        if self.cell == self.start_real_cell:
            self._already_died = True
            self.state = GhostState.LEAVING_HOME
            self.cell = self.start_cell
            self.direction = None
            self._next_direction = None
            self._next_cell = None
            self._update_ghost()

    def _assign_next_move(self):
        possible_moves = self._get_possible_moves(self._target_cell)

        if len(possible_moves) == 0:
            self._go_back()
            possible_moves = self._get_possible_moves(self._target_cell)

        if self.goal_cell is None:
            self._next_direction, self._next_cell = random.choice(list(possible_moves.items()))
        else:
            self._next_direction, self._next_cell = self._get_closest_move(possible_moves)

    @abstractmethod
    def _get_chase_cell(self):
        pass

    @abstractmethod
    def get_dots_to_leave(self):
        pass

    def set_dead_text(self, score):
        self._dead_text = TextUtils.get_score_text(score)

    def _handle_collision(self):
        if self._collides(self.manager.game.pacman.rect.center):
            if self._can_die():
                self.state = GhostState.DEAD
                self._reverse_direction = True
                self.manager.handle_ghost_dead(self)
            elif self._can_kill():
                self.manager.handle_pacman_dead()

    def _can_die(self):
        is_frightened = self.manager.current_mode == GhostMode.FRIGHTENED
        is_not_dead = not self.state == GhostState.DEAD
        return is_frightened and not self._already_died and is_not_dead

    def _can_kill(self):
        is_not_dead = not self.state == GhostState.DEAD
        chase_or_scatter = self.manager.current_mode in [GhostMode.CHASE, GhostMode.SCATTER]
        already_dead = self._already_died
        return is_not_dead and (chase_or_scatter or already_dead)

    def _collides(self, center):
        self_x, self_y = self.rect.center
        center_x, center_y = center

        return center_x - self.COLLISION_OFFSET <= self_x <= center_x + self.COLLISION_OFFSET \
            and center_y - self.COLLISION_OFFSET <= self_y <= center_y + self.COLLISION_OFFSET

    def _handle_reverse_direction(self):
        if self._reverse_direction and self._can_reverse():
            self._go_back()

        self._reverse_direction = False

    def _go_back(self):
        self._next_direction = self.REVERSE[self.direction]
        self._next_cell = self._previous_cell
        self._previous_cell = self.cell

    def _can_reverse(self):
        is_previous = self._previous_cell is not None
        is_direction = self.direction is not None
        is_active = self.state == GhostState.ACTIVE

        return is_previous and is_direction and is_active

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

    def _animated_movement(self, speed):
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
        self.state = GhostState.LEAVING_HOME

    def _get_closest_move(self, moves):
        items = moves.items()
        if len(items) == 0:
            return None, None

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
        is_walkable = self.is_cell_walkable(next_cell)
        can_move_up = not (direction == Direction.UP and self._target_cell in self.NO_MOVE_UP_CELLS)
        is_not_backward = not (self.direction and direction == self.REVERSE.get(self.direction))

        return is_walkable and can_move_up and is_not_backward

    def _get_icon_name(self):
        if self._can_show_frightened_icon():
            if self.manager.should_animate_icon():
                icon_id = self._icon_counter + 1
                if self._last_icon_update is None:
                    self._last_icon_update = time.time()
                elif TimeUtils.elapsed(self._last_icon_update) >= self.GHOST_FRIGHT_ICON_TIME:
                    self._icon_counter = (self._icon_counter + 1) % self.GHOST_FRIGHT_ICONS
                    self._last_icon_update = time.time()

                icon = f"ghost-vulnerable-{icon_id}"
            else:
                icon = f"ghost-vulnerable-1"
        else:
            direction = self.direction if self.direction else self.DEFAULT_DIRECTION
            direction_in_lowercase = direction.name.lower()
            name = "dead" if self.state == GhostState.DEAD else self.__class__.__name__.lower()
            icon = f"ghost-{name}-{direction_in_lowercase}"

        return icon

    def _can_show_frightened_icon(self):
        is_mode_frightened = self.manager.current_mode == GhostMode.FRIGHTENED
        is_not_dead = not self.state == GhostState.DEAD
        can_die = not self._already_died
        is_not_idle = self.state != GhostState.IDLE

        return is_mode_frightened and is_not_dead and can_die and is_not_idle

    def is_cell_walkable(self, cell):
        if not CellMap.get_instance().cell_exists(cell):
            return False

        cell_type = CellMap.get_instance().get_cell_type(cell)
        if self._can_go_through_gate():
            return cell_type in [Cell.SPACE, Cell.TUNNEL, Cell.SPACE_GATE]
        else:
            return cell_type in [Cell.SPACE, Cell.TUNNEL]

    def _can_go_through_gate(self):
        return self.state in [GhostState.LEAVING_HOME, GhostState.DEAD]

    def render(self, screen):
        self._render_hint(screen)
        if self.manager.game.state == GameState.EAT_GHOST_FREEZE and self._dead_text:
            position = CellMap.get_cell_position(self.cell)
            screen.blit(self._dead_text, self._dead_text.get_rect(center=position))
        else:
            super().render(screen)

    def _render_hint(self, screen):
        if self.goal_cell is not None:
            x, y = CellMap.get_cell_position(self.goal_cell, center=False)
            size = CellMap.CELL_SIZE_IN_PIXELS
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, size, size), 2)
