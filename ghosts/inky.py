from ghosts.ghost import Ghost


class Inky(Ghost):
    NAME = "inky"

    def __init__(self, state):
        super().__init__(self.NAME, state)
