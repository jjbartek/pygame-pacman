import math
import time

from cell_map import CellMap
from direction import Direction
from movable_entity import MovableEntity
from utils.file_utils import FileUtils


class Ghost(MovableEntity):
    DEFAULT_GHOST_MOVE_TIME = 160
    DEFAULT_DIRECTION = Direction.UP
    FIRST_CELL = (13.5, 14)
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

    def __init__(self, name, start_cell, destined_cell, game):
        super().__init__()
        self.name = name
        self.game = game
        self.start_cell = start_cell
        self.default_destination_cell = destined_cell
        self.cell = self.start_cell
        self.direction = self.DEFAULT_DIRECTION
        self.destined_cell = self.default_destination_cell
        self.image = FileUtils.get_image(self._get_icon_name())
        self._speed = self.DEFAULT_GHOST_MOVE_TIME
        self._next_cell = None
        self._next_direction = None

        self._update_position(CellMap.get_cell_position(self.cell))

    def update(self):
        if self._active:
            self._move()
            self.image = FileUtils.get_image(self._get_icon_name())
            self._detect_collision()

    def reset(self):
        super().reset()
        self.cell = self.start_cell
        self.direction = self.DEFAULT_DIRECTION
        self.destined_cell = self.default_destination_cell
        self.image = FileUtils.get_image(self._get_icon_name())
        self._speed = self.DEFAULT_GHOST_MOVE_TIME
        self._next_cell = None
        self._next_direction = None

        self._update_position(CellMap.get_cell_position(self.cell))

    def _detect_collision(self):
        self_x, self_y = self.rect.center
        pacman_x, pacman_y = self.game.pacman.rect.center

        if pacman_x - self.COLLISION_OFFSET <= self_x <= pacman_x + self.COLLISION_OFFSET \
                and pacman_y - self.COLLISION_OFFSET <= self_y <= pacman_y + self.COLLISION_OFFSET:
            self.game.pacman_dead()

    def _move(self):
        speed = self._speed
        if self._target_cell and self._target_cell in self.SLOW_CELLS:
            speed *= 1.5

        if self._moving:
            self._slow_movement(speed)
        else:
            self.direction = self._next_direction
            self._target_cell = self._next_cell
            self._move_start_time = time.time()
            self._moving = True

            possible_moves = self._get_possible_moves()
            self._next_direction, self._next_cell = self._get_closest_move(possible_moves)
            self._slow_movement(speed)

    def activate(self):
        self._next_cell = CellMap.get_instance().get_next_cell(self.cell, Direction.LEFT)
        self._next_direction = Direction.LEFT
        self._active = True

    def _get_closest_move(self, moves):
        return min(moves.items(), key=lambda move: self._get_sort_key(move))

    def _get_sort_key(self, item):
        direction, cell = item
        return self._get_distance_to_destined(cell), self.DIRECTION_PRIORITY[direction]

    def _get_distance_to_destined(self, cell):
        x, y = cell
        destined_x, destined_y = self.destined_cell
        return math.sqrt((x - destined_x) ** 2 + (y - destined_y) ** 2)

    def _get_possible_moves(self):
        moves = {}
        for direction in Direction:
            next_cell = CellMap.get_instance().get_next_cell(self._next_cell, direction)
            if self._can_move_to_cell(direction, next_cell):
                moves[direction] = next_cell

        return moves

    def _can_move_to_cell(self, direction, next_cell):
        return direction != self.REVERSE[self.direction] \
            and CellMap.get_instance().is_cell_walkable(next_cell) \
            and not (direction == Direction.UP and self._next_cell in self.NO_MOVE_UP_CELLS)

    def _get_icon_name(self):
        direction_in_lowercase = self.direction.name.lower()

        return f"ghost-{self.name}-{direction_in_lowercase}"
