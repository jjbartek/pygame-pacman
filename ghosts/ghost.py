import time

from direction import Direction
from movable_entity import MovableEntity
from utils.image_utils import ImageUtils


class Ghost(MovableEntity):
    images = {}
    DEFAULT_GHOST_MOVE_TIME = 160
    DEFAULT_DIRECTION = Direction.UP

    # lowest value - highest priority
    DIRECTION_PRIORITY = {
        Direction.UP: 0,
        Direction.LEFT: 1,
        Direction.DOWN: 2,
        Direction.RIGHT: 3
    }

    def __init__(self, name, state):
        super().__init__()
        self.name = name
        self.state = state
        self.start_cell = self.state.level.ghost_home_cells[name]
        self.default_destination_cell = self.state.level.ghost_destination_cells[name]
        self.cell = self.start_cell
        self.direction = self.DEFAULT_DIRECTION
        self.destined_cell = self.default_destination_cell
        self.image = self.get_image(self._get_icon_name())
        self._speed = self.DEFAULT_GHOST_MOVE_TIME
        self._next_cell = None
        self._next_direction = None

        self._update_position(self.state.level.get_cell_position(self.cell))

    def update(self):
        if self._active is True:
            self._move()
            self.image = self.get_image(self._get_icon_name())

    def _move(self):
        if self._moving:
            self._slow_movement()
        else:
            self.direction = self._next_direction
            self._target_cell = self._next_cell
            self._move_start_time = time.time()
            self._moving = True

            possible_moves = self._get_possible_moves()
            self._next_direction, self._next_cell = self._get_closest_move(possible_moves)
            self._slow_movement()

    def activate(self):
        self._next_cell = self._get_next_cell(self.cell, Direction.LEFT)
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
        return abs(x - destined_x) + abs(y - destined_y)

    def _get_possible_moves(self):
        moves = {}
        for direction in Direction:
            next_cell = self._get_next_cell(self._next_cell, direction)
            if next_cell != self.cell and self._is_cell_walkable(next_cell):
                moves[direction] = next_cell

        return moves

    def _get_icon_name(self):
        direction_in_lowercase = self.direction.name.lower()

        return f"ghost-{self.name}-{direction_in_lowercase}"

    @classmethod
    def get_image(cls, name):
        if name not in cls.images:
            cls.images[name] = ImageUtils.get(name)

        return cls.images[name]
