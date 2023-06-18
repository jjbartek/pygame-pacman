from entities.ghost import Ghost


class Clyde(Ghost):
    START_CELL = (15.5, 17)
    START_REAL_CELL = (15, 17)
    SCATTER_CELL = (0, 35)
    COLOR = (255, 184, 82)
    MAX_DISTANCE = 8

    def __init__(self, manager):
        super().__init__(self.START_CELL, self.START_REAL_CELL, self.SCATTER_CELL, self.COLOR, manager)

    def _get_chase_cell(self):
        if self._is_in_pacman_range():
            chase_cell = self.scatter_cell
        else:
            chase_cell = self.manager.game.pacman.cell

        return chase_cell

    def _is_in_pacman_range(self):
        pacman_x, pacman_y = self.manager.game.pacman.cell
        self_x, self_y = self.cell

        return pacman_x - self.MAX_DISTANCE <= self_x <= pacman_x + self.MAX_DISTANCE \
            and pacman_y - self.MAX_DISTANCE <= self_y <= pacman_y + self.MAX_DISTANCE
