from ghosts.ghost import Ghost


class Pinky(Ghost):
    NAME = "pinky"
    START_CELL = (13.5, 17)
    DESTINED_CELL = (1, 0)

    def __init__(self, game):
        super().__init__(self.NAME, self.START_CELL, self.DESTINED_CELL, game)
