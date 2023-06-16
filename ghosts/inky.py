from cell_map import CellMap
from direction import Direction
from ghosts.ghost import Ghost
from ghosts.ghost_modes import GhostModes


class Inky(Ghost):
    NAME = "inky"
    START_CELL = (11.5, 17)
    START_REAL_CELL = (12, 17)
    SCATTER_CELL = (0, 35)
    COLOR = (0, 255, 255)

    PACMAN_OFFSET = {
        Direction.UP: (0, -2),
        Direction.DOWN: (0, 2),
        Direction.LEFT: (-2, 0),
        Direction.RIGHT: (2, 0),
    }

    def __init__(self, manager):
        super().__init__(self.NAME, self.START_CELL, self.START_REAL_CELL, self.SCATTER_CELL, self.COLOR, manager)

    def get_chase_cell(self):
        blinky_x, blinky_y = self.manager.blinky.cell
        pacman_x, pacman_y = self.manager.game.pacman.cell
        offset_x, offset_y = self.PACMAN_OFFSET[self.manager.game.pacman.direction]
        plane_x, plane_y = CellMap.CELLS_PER_PLANE
        intermediate_x, intermediate_y = (pacman_x + offset_x) % plane_x, (pacman_y + offset_y) % plane_y
        distance_blinky_x, distance_blinky_y = blinky_x - intermediate_x, blinky_y - intermediate_y
        result = (intermediate_x - distance_blinky_x) % plane_x, (intermediate_y - distance_blinky_y) % plane_y

        return result
