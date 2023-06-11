from ghosts.ghost import Ghost


class Inky(Ghost):
    NAME = "inky"
    START_CELL = (11.5, 17)
    DESTINED_CELL = (0, 35)

    def __init__(self, board):
        super().__init__(self.NAME, self.START_CELL, self.DESTINED_CELL, board)