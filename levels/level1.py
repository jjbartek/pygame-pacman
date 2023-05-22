from .level import Level


class Level1(Level):
    def __init__(self):
        super().__init__(1, "board", "level1", (0, 0), 20)
