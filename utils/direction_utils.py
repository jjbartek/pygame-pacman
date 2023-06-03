from enum import Enum

import pygame


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class DirectionUtils:
    POSITION_MAPPING = {
        Direction.UP: (0, 1),
        Direction.DOWN: (0, -1),
        Direction.RIGHT: (0, 1),
        Direction.LEFT: (0, -1),
    }

    KEY_TO_DIRECTION_MAPPING = {
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN
    }

    @classmethod
    def next_position(cls, current_position, direction):
        return tuple(map(sum, zip(current_position, cls.POSITION_MAPPING.get(direction))))
