from ghosts.ghost import Ghost


class Blinky(Ghost):
    NAME = "blinky"
    START_CELL = (13.5, 14)
    DESTINED_CELL = (26, 0)

    def __init__(self, board):
        super().__init__(self.NAME, self.START_CELL, self.DESTINED_CELL, board)
