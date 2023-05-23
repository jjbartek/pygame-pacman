from direction import Direction


class Utils:
    position_mapping = {
        Direction.UP: (0, 1),
        Direction.DOWN: (0, -1),
        Direction.RIGHT: (0, 1),
        Direction.LEFT: (0, -1),
    }

    @staticmethod
    def next_position(direction, current_position):
        return tuple(map(sum, zip(current_position, Utils.position_mapping.get(direction))))
