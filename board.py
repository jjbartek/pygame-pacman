from cell import Cell
from elements.dot import Dot
from elements.energizer import Energizer
import pygame

from pacman import Pacman


class Board:
    def __init__(self, image, position, structure, square_size, surface):
        self.image = image
        self.position = position
        self.structure = structure
        self.square_size = square_size
        self.surface = surface

        self.elements = pygame.sprite.Group()
        self.pacman = None
        self.x_size = None
        self.y_size = None
        self.map = None

        self._load_map()

    def show(self):
        self.surface.blit(self.image, (0, 0))
        self.elements.draw(self.surface)
        self.pacman.show(self.surface)

    def update(self, events):
        keys = pygame.key.get_pressed()
        self.pacman.update(keys)

    def _load_map(self):
        x = 0
        y = 0
        self.map = []
        for line in self.structure:
            line_list = []
            x = 0
            for char in line.strip():
                if char == '|':
                    line_list.append(Cell.WALL)
                elif char == '-':
                    line_list.append(Cell.SPACE)
                elif char == '*':
                    line_list.append(Cell.SPACE)
                    new_dot = Dot(self.calculate_position((x, y)))
                    self.elements.add(new_dot)
                elif char == "&":
                    line_list.append(Cell.SPACE)
                    new_energizer = Energizer(self.calculate_position((x, y)))
                    self.elements.add(new_energizer)
                elif char == '+':
                    line_list.append(Cell.SPACE_TELEPORT)
                x += 1
            self.map.append(line_list)
            y += 1
        self.x_size = x
        self.y_size = y

        self.pacman = Pacman(self)

    def calculate_position(self, cell):
        x, y = cell
        x_offset, y_offset = self.position
        x_position = x * self.square_size + self.square_size / 2 + x_offset
        y_position = y * self.square_size + self.square_size / 2 + y_offset
        return x_position, y_position
