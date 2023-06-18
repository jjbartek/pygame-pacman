from enum import Enum


class GameState(Enum):
    GAME_START = 1
    PLAYING = 2
    GHOST_DEAD = 3
    DEAD = 4
    DEAD_END = 5
    LEVEL_END = 6
