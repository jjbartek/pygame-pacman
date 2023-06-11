import time
from enum import Enum

from cell_map import CellMap
from game_info import GameInfo
from level import Level
from managers.ghosts_manager import GhostsManager
from pacman import Pacman
from managers.collectibles_manager import CollectiblesManager
from stages.stage import Stage
from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


class FreezeReasons(Enum):
    PACMAN_DEAD = 1
    LEVEL_END = 2


class GameStage(Stage):
    PACMAN_DEAD_FREEZE_TIME = 1500
    BACKGROUND_CORDS = (0, 0)
    BACKGROUND_NAME = "board"
    MIN_LEVEL = 1
    MAX_LEVEL = 1

    def __init__(self):
        super().__init__()
        self.level_id = 0
        self.level = None
        self.collectibles = None
        self.ghosts = None
        self.pacman = None
        self.score = 0
        self.freeze = False
        self.freeze_start = None
        self.freeze_reason = None
        self.game_info = None
        self.background = FileUtils.get_image(self.BACKGROUND_NAME)

        CellMap.get_instance()

    def start_game(self):
        self.level_id = self.MIN_LEVEL
        self.level = Level(self)
        self.collectibles = CollectiblesManager(self)
        self.pacman = Pacman(self)
        self.ghosts = GhostsManager(self)
        self.game_info = GameInfo(self)

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

    def update(self, events, key_pressed):
        self.collectibles.update()
        self.pacman.update(key_pressed)
        self.ghosts.update()

        if self.freeze and self.freeze_reason == FreezeReasons.PACMAN_DEAD \
                and TimeUtils.time_elapsed_since(self.freeze_start) >= self.PACMAN_DEAD_FREEZE_TIME:
            self.freeze = False
            self.freeze_start = None
            self.freeze_reason = None
            self.pacman.lives -= 1
            self.pacman.reset()
            self.ghosts.reset()

    def render(self, screen):
        self._render_background(screen)
        self.collectibles.render(screen)
        self.pacman.render(screen)
        self.ghosts.render(screen)
        self.game_info.render(screen)

    def _render_background(self, screen):
        screen.blit(self.background, self.BACKGROUND_CORDS)
