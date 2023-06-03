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

    def render(self):
        self.state.screen.blit(self.image, self.rect)

    def _move(self):
        pass

    def _get_next_cell(self, direction):
        if self._active is False:
            self._convert_cell_to_integers()
        return tuple(map(sum, zip(self.cell, self.POSITION_MAPPING.get(direction.value))))

    def _convert_cell_to_integers(self):
        # this is necessary for starting cell - which may have decimal values
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
        return 0 <= x <= x_cells-1 and 0 <= y <= y_cells-1

    def _is_cell_walkable(self, cell):
        x, y = cell
        cell_type = self.state.level.map[y][x]
        return cell_type is Cell.SPACE or cell_type is Cell.TELEPORT
