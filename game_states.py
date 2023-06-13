from enum import Enum


class GameStates(Enum):
    GAME_START = 1
    PLAYING = 2
    DEAD = 3
    DEAD_END = 4
    LEVEL_END = 5