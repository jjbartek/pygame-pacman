from ghosts.ghost import Ghost


class Clyde(Ghost):
    NAME = "clyde"

    def __init__(self, state):
        super().__init__(self.NAME, state)
