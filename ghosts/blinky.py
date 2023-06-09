from ghosts.ghost import Ghost


class Blinky(Ghost):
    NAME = "blinky"

    def __init__(self, state):
        super().__init__(self.NAME, state)
