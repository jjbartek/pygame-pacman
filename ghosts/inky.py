from cell_map import CellMap
from direction import Direction
from ghosts.ghost import Ghost
from ghosts.ghost_modes import GhostModes


class Inky(Ghost):
    NAME = "inky"
    START_CELL = (11.5, 17)
    START_REAL_CELL = (12, 17)
    DEFAULT_GOAL_CELL = (0, 35)

    PACMAN_OFFSET = {
        Direction.UP: (0, -4),
        Direction.DOWN: (0, 4),
        Direction.LEFT: (-4, 0),
        Direction.RIGHT: (4, 0),
    }

    def __init__(self, manager):
        super().__init__(self.NAME, self.START_CELL, self.START_REAL_CELL, self.DEFAULT_GOAL_CELL, manager)

    def get_chase_cell(self):
        pacman_x, pacman_y = self.manager.game.pacman.cell
        offset_x, offset_y = self.PACMAN_OFFSET[self.manager.game.pacman.direction]
        plane_x_size, plane_y_size = CellMap.CELLS_PER_PLANE

        return (pacman_x + offset_x) % plane_x_size, (pacman_y + offset_y) % plane_y_size
