import time
from enum import Enum

from managers.ghosts_manager import GhostsManager
from pacman import Pacman
from utils.level_utils import LevelUtils
from managers.collectibles_manager import CollectiblesManager
from utils.time_utils import TimeUtils


class FreezeReasons(Enum):
    PACMAN_DEAD = 1
    LEVEL_END = 2


class State:
    PACMAN_DEAD_FREEZE_TIME = 3000

    def __init__(self):
        self.is_running = False
        self.level_id = LevelUtils.MIN_LEVEL
        self.level = LevelUtils.get_level(self.level_id)
        self.collectibles = CollectiblesManager()
        self.ghosts = GhostsManager()
        self.pacman = Pacman()
        self.screen = None
        self.score = 0
        self.freeze = False
        self.freeze_start = None
        self.freeze_reason = None

    def add_score(self, score):
        # check if all collected
        self.score += score
        # print(self.score)

    def pacman_dead(self):
        if self.pacman.lives > 1:
            self.freeze = True
            self.freeze_start = time.time()
            self.freeze_reason = FreezeReasons.PACMAN_DEAD
        else:
            self.end_game()

    def end_game(self):
        pass

    def update(self):
        if self.freeze and self.freeze_reason == FreezeReasons.PACMAN_DEAD \
                and TimeUtils.time_elapsed_since(self.freeze_start) >= self.PACMAN_DEAD_FREEZE_TIME:
            self.freeze = False
            self.freeze_start = None
            self.freeze_reason = None
            self.pacman.lives -= 1
            self.pacman.reset()
            self.ghosts.reset()
