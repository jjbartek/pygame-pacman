from ghosts.ghost import Ghost
from ghosts.ghost_modes import GhostModes


class Blinky(Ghost):
    NAME = "blinky"
    START_CELL = (13.5, 14)
    START_REAL_CELL = (13, 14)
    DEFAULT_GOAL_CELL = (26, 0)

    def __init__(self, manager):
        super().__init__(self.NAME, self.START_CELL, self.START_REAL_CELL, self.DEFAULT_GOAL_CELL, manager)

    def get_chase_cell(self):
        return self.manager.game.pacman.cell
