from entities.ghost import Ghost


class Blinky(Ghost):
    NAME = "blinky"
    START_CELL = (13.5, 14)
    START_REAL_CELL = (13, 14)
    SCATTER_CELL = (26, 0)
    COLOR = (255, 0, 0)

    def __init__(self, manager):
        super().__init__(self.NAME, self.START_CELL, self.START_REAL_CELL, self.SCATTER_CELL, self.COLOR, manager)

    def _get_chase_cell(self):
        return self.manager.game.pacman.cell
