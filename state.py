from managers.ghosts_manager import GhostsManager
from pacman import Pacman
from utils.level_utils import LevelUtils
from managers.collectibles_manager import CollectiblesManager


class State:
    def __init__(self):
        self.is_running = False
        self.level_id = LevelUtils.MIN_LEVEL
        self.level = LevelUtils.get_level(self.level_id)
        self.collectibles = CollectiblesManager()
        self.ghosts = GhostsManager()
        self.pacman = Pacman()
        self.screen = None
        self.score = 0

    def add_score(self, score):
        # check if all collected
        self.score += score
        print(self.score)
