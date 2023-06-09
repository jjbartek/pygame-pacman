from enum import Enum


class Cell(Enum):
    WALL = 1
    SPACE = 2
    SPACE_GATE = 3
    DOT = 4
    ENERGIZER = 5
    TUNNEL = 6
