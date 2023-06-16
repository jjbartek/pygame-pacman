import random
import time

import pygame

from ghosts.ghost_modes import GhostModes
from ghosts.inky import Inky
from ghosts.blinky import Blinky
from ghosts.clyde import Clyde
from ghosts.pinky import Pinky
from utils.time_utils import TimeUtils


class GhostsManager:
    def __init__(self, game):
        self.game = game
        self.group = pygame.sprite.Group()
        self.blinky = Blinky(self)
        self.pinky = Pinky(self)
        self.inky = Inky(self)
        self.clyde = Clyde(self)
        self.mode = GhostModes.CHASE
        self._timer = time.time()


        self.group.add(self.blinky)
        self.group.add(self.pinky)
        self.group.add(self.inky)
        self.group.add(self.clyde)

        self.inky.activate()

    def update(self):
        for ghost in self.group:
            # if TimeUtils.time_elapsed(self._timer) > 10000:
                # if self.mode == GhostModes.SCATTER:
                #     self.update_mode(GhostModes.CHASE)
                # else:
                #     self.update_mode(GhostModes.SCATTER)
                # ghost.reverse_direction()
                # self._timer = time.time()
            ghost.update()

    def update_mode(self, mode):
        for ghost in self.group:
            ghost.reverse_direction()
        self.mode = mode

    def render(self, screen):
        for ghost in self.group:
            ghost.render(screen)

    def reset(self):
        for ghost in self.group:
            ghost.reset()

        self.blinky.activate()
