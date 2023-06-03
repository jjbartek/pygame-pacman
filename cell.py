from enum import Enum


class Cell(Enum):
    WALL = 1
    SPACE = 2
    DOT = 3
    ENERGIZER = 4
    TELEPORT = 5
