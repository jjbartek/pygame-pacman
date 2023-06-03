import pygame

from cell import Cell
from collectibles.dot import Dot
from collectibles.energizer import Energizer
from utils.image_utils import ImageUtils


class Level:
    BACKGROUND_CORDS = (0, 0)
    CHAR_CELL_MAP = {
        "|": Cell.WALL,
        "-": Cell.SPACE,
        "*": Cell.SPACE,
        "&": Cell.SPACE,
        "+": Cell.TELEPORT
    }

    CHAR_COLLECTIBLE_MAP = {
        "*": Dot,
        "&": Energizer
    }

    def __init__(self, level_id, background_name, structure, cells_per_plane, dimensions_in_pixels, cell_size_in_pixels,
                 default_cell, offset):
        self.id = level_id
        self.background_name = background_name
        self.structure = structure
        self.cells_per_plane = cells_per_plane
        self.dimensions_in_pixels = dimensions_in_pixels
        self.cell_size_in_pixels = cell_size_in_pixels
        self.default_cell = default_cell
        self.offset = offset

        self.state = None
        self.surface = None
        self.map = []
        self._initialized = False

    def initialize(self, state):
        if self._initialized is True:
            return

        self.state = state
        self.surface = ImageUtils.get(self.background_name)
        self._load_map()
        self._initialized = True

    def render(self):
        self.state.screen.blit(self.surface, self.BACKGROUND_CORDS)

    def _load_map(self):
        x_size, y_size = self.cells_per_plane

        self.map = []
        for y in range(y_size):
            row = []
            for x in range(x_size):
                cell_pos = (x, y)
                char = self._get_char_at_position(cell_pos)

                if char in self.CHAR_COLLECTIBLE_MAP:
                    collectible_class = self.CHAR_COLLECTIBLE_MAP[char]
                    self._add_collectible_at_cell_position(collectible_class, cell_pos)

                row.append(self.CHAR_CELL_MAP[char])
            self.map.append(row)

    def _add_collectible_at_cell_position(self, collectible_class, cell_pos):
        real_position = self.get_cell_position(cell_pos)
        collectible = collectible_class(real_position)
        self.state.collectibles.add(collectible)

    def get_cell_position(self, cell_pos):
        x, y = cell_pos
        x_offset, y_offset = self.offset
        cell_size = self.cell_size_in_pixels

        x_position = x * cell_size + cell_size / 2 + x_offset
        y_position = y * cell_size + cell_size / 2 + y_offset

        return x_position, y_position

    def _get_char_at_position(self, pos):
        x, y = pos
        x_length = self.cells_per_plane[0]
        pos_in_structure = y * (x_length+1) + x

        return self.structure[pos_in_structure]