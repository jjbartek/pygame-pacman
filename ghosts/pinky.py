from ghosts.ghost import Ghost


class Pinky(Ghost):
    NAME = "pinky"

    def __init__(self, state):
        super().__init__(self.NAME, state)
