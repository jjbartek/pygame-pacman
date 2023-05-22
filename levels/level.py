import os


class Level:
    def __init__(self, number, board_name, structure_name, position, square_size):
        self.number = number
        self.position = position
        self.square_size = square_size
        self.background = os.path.join(os.getcwd(), 'resources', 'images', f"{board_name}.png")
        self.structure = os.path.join(os.getcwd(), 'resources', 'levels', f"{structure_name}.txt")
