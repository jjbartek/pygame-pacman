from ghosts.ghost import Ghost


class Clyde(Ghost):
    NAME = "clyde"
    START_CELL = (15.5, 17)
    DESTINED_CELL = (0, 35)

    def __init__(self, board):
        super().__init__(self.NAME, self.START_CELL, self.DESTINED_CELL, board)
