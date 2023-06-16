from ghosts.ghost import Ghost
from ghosts.ghost_modes import GhostModes


class Pinky(Ghost):
    NAME = "pinky"
    START_CELL = (13.5, 17)
    START_REAL_CELL = (13, 17)
    DEFAULT_GOAL_CELL = (1, 0)

    def __init__(self, manager):
        super().__init__(self.NAME, self.START_CELL, self.START_REAL_CELL, self.DEFAULT_GOAL_CELL, manager)

    def get_chase_cell(self):
        return self.default_goal_cell
