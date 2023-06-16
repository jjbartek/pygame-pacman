from ghosts.ghost import Ghost
from ghosts.ghost_modes import GhostModes


class Clyde(Ghost):
    NAME = "clyde"
    START_CELL = (15.5, 17)
    START_REAL_CELL = (15, 17)
    DEFAULT_GOAL_CELL = (0, 35)

    def __init__(self, manager):
        super().__init__(self.NAME, self.START_CELL, self.START_REAL_CELL, self.DEFAULT_GOAL_CELL, manager)

    def get_chase_cell(self):
        return self.default_goal_cell