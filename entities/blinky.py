from entities.ghost import Ghost
from enums.ghost_state import GhostState


class Blinky(Ghost):
    START_CELL = (13.5, 14)
    START_REAL_CELL = (13, 14)
    SCATTER_CELL = (26, 0)
    COLOR = (255, 0, 0)
    DOTS_TO_LEAVE = 0
    DOTS_AFTER_DEATH = 0

    def __init__(self, manager):
        super().__init__(self.START_CELL, self.START_REAL_CELL, self.SCATTER_CELL, self.COLOR, self.DOTS_AFTER_DEATH,
                         manager)

    def _get_chase_cell(self):
        return self.manager.game.pacman.cell

    def _can_go_through_gate(self):
        return False

    def get_dots_to_leave(self):
        return self.DOTS_TO_LEAVE
