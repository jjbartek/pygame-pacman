from cell import Cell
from dot import Dot
import pygame


class Board:
    def __init__(self, structure, square_size):
        self.structure = structure
        self.square_size = square_size
        self.dots = pygame.sprite.Group()
        self.x_size = None
        self.y_size = None
        self.map = None

        self._load_map()

    def _load_map(self):
        x = 0
        y = 0
        self.map = []
        for line in self.structure.split('\n'):
            line_list = []
            y = 0
            for char in line:
                if char is '|':
                    line_list.append(Cell.WALL)
                elif char is '-':
                    line_list.append(Cell.SPACE)
                elif char is '*':
                    line_list.append(Cell.SPACE)
                    new_dot = Dot((x, y))
                    # add to sprite
                elif char is '+':
                    line_list.append(Cell.SPACE_TELEPORT)
                y += 1
            self.map.append(line_list)
            x += 1
        self.x_size = x
        self.y_size = y