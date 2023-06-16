from cell import Cell
from collectibles.dot import Dot
from collectibles.energizer import Energizer
from direction import Direction
from utils.file_utils import FileUtils


class CellMap:
    _instance = None
    CELLS_PER_PLANE = (28, 36)
    CELL_SIZE_IN_PIXELS = 20
    CHAR_CELL_MAP = {
        "|": Cell.WALL,
        "-": Cell.SPACE,
        "*": Cell.SPACE,
        "&": Cell.SPACE,
        "+": Cell.TUNNEL,
        "%": Cell.SPACE_GATE
    }
    CHAR_COLLECTIBLE_MAP = {
        "*": Dot,
        "&": Energizer
    }
    POSITION_MAPPING = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.RIGHT: (1, 0),
        Direction.LEFT: (-1, 0),
    }

    def __init__(self):
        self.collectibles = {
            Dot: [],
            Energizer: []
        }
        self.count = 0
        self.map = []

        self._load_map()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def _load_map(self):
        x_size, y_size = self.CELLS_PER_PLANE
        structure = FileUtils.get_structure()

        self.map = []
        for y in range(y_size):
            row = []
            for x in range(x_size):
                cell_pos = (x, y)
                char = self._get_char_at_position(cell_pos, structure)

                if char in self.CHAR_COLLECTIBLE_MAP:
                    collectible_class = self.CHAR_COLLECTIBLE_MAP[char]
                    self.collectibles[collectible_class].append(cell_pos)
                    self.count += 1

                row.append(self.CHAR_CELL_MAP[char])
            self.map.append(row)

    def _get_char_at_position(self, pos, structure):
        x, y = pos
        x_length, _ = self.CELLS_PER_PLANE
        pos_in_structure = y * (x_length + 1) + x

        return structure[pos_in_structure]

    def get_cell_type(self, cell):
        x, y = cell
        return self.map[int(y)][int(x)]

    def get_next_cell(self, current_cell, direction):
        x, y = current_cell
        current_cell = int(x), int(y)
        next_cell = tuple(map(sum, zip(current_cell, self.POSITION_MAPPING.get(direction))))
        if self._is_going_through_tunnel(current_cell, next_cell):
            x_cells, y_cells = self.CELLS_PER_PLANE
            x, y = next_cell
            next_cell = x % x_cells, y % y_cells
        return next_cell

    def _is_going_through_tunnel(self, current_cell, next_cell):
        return self.get_cell_type(current_cell) == Cell.TUNNEL and not self.cell_exists(next_cell)

    @classmethod
    def cell_exists(cls, cell):
        x, y = cell
        x_cells, y_cells = cls.CELLS_PER_PLANE
        return 0 <= x <= x_cells - 1 and 0 <= y <= y_cells - 1

    @classmethod
    def get_cell_position(cls, cell_pos, center=True):
        x, y = cell_pos
        cell_size = cls.CELL_SIZE_IN_PIXELS

        x_position = x * cell_size
        y_position = y * cell_size

        if center:
            x_position += cell_size / 2
            y_position += cell_size / 2

        return x_position, y_position
