from cell_map import CellMap
from enums.direction import Direction
from entities.ghost import Ghost


class Pinky(Ghost):
    START_CELL = (13.5, 17)
    START_REAL_CELL = (13, 17)
    SCATTER_CELL = (1, 0)
    COLOR = (255, 184, 255)

    PACMAN_OFFSET = {
        Direction.UP: (0, -4),
        Direction.DOWN: (0, 4),
        Direction.LEFT: (-4, 0),
        Direction.RIGHT: (4, 0),
    }

    def __init__(self, manager):
        super().__init__(self.START_CELL, self.START_REAL_CELL, self.SCATTER_CELL, self.COLOR, manager)

    def _get_chase_cell(self):
        pacman_x, pacman_y = self.manager.game.pacman.cell
        offset_x, offset_y = self.PACMAN_OFFSET[self.manager.game.pacman.direction]
        plane_x_size, plane_y_size = CellMap.CELLS_PER_PLANE

        return (pacman_x + offset_x) % plane_x_size, (pacman_y + offset_y) % plane_y_size
