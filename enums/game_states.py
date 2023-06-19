from enum import Enum


class GameState(Enum):
    GAME_START = 1
    PLAYING = 2
    EAT_GHOST_FREEZE = 3
    EAT_FRUIT_FREEZE = 4
    DEAD = 5
    DEAD_END = 6
    LEVEL_END = 7
