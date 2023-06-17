import time

import pygame

from enums.ghost_mode import GhostMode
from entities.inky import Inky
from entities.blinky import Blinky
from entities.clyde import Clyde
from entities.pinky import Pinky
from utils.time_utils import TimeUtils


class GhostsManager:
    FRIGHTENED_TIME = 10000

    def __init__(self, game):
        self.game = game
        self.group = pygame.sprite.Group()
        self.mode = GhostMode.CHASE
        self.blinky = Blinky(self)
        self.pinky = Pinky(self)
        self.inky = Inky(self)
        self.clyde = Clyde(self)
        self._mode_start_time = time.time()
        self._channel = pygame.mixer.Channel(3)
        self._elapsed_since_start = None

        self.group.add(self.blinky)
        self.group.add(self.pinky)
        self.group.add(self.inky)
        self.group.add(self.clyde)

        self.clyde.activate()
        self.pinky.activate()
        self.inky.activate()
        self.blinky.activate()

    def update(self):
        if self.mode == GhostMode.FRIGHTENED and TimeUtils.time_elapsed(self._mode_start_time) > self.FRIGHTENED_TIME:
            self.update_mode(GhostMode.CHASE)

        for ghost in self.group:
            ghost.update()

    def update_mode(self, mode):
        for ghost in self.group:
            if mode != self.mode and self.mode != GhostMode.FRIGHTENED:
                ghost.reverse_direction()
            ghost.reset_dead()

        self.mode = mode
        self._mode_start_time = time.time()

    def render(self, screen):
        for ghost in self.group:
            ghost.render(screen)

    def reset(self):
        for ghost in self.group:
            ghost.reset()

        self.clyde.activate()
        self.pinky.activate()
        self.inky.activate()
        self.blinky.activate()

    def pause(self):
        self._elapsed_since_start = time.time() - self._mode_start_time

    def unpause(self):
        self._mode_start_time = time.time() - self._elapsed_since_start
        self._elapsed_since_start = None
