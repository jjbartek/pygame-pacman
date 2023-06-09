from direction import Direction
from movable_entity import MovableEntity
from utils.image_utils import ImageUtils


class Ghost(MovableEntity):
    images = {}
    DEFAULT_GHOST_MOVE_TIME = 110
    DEFAULT_DIRECTION = Direction.UP

    def __init__(self, name, state):
        super().__init__()
        self.name = name
        self.state = state
        self.start_cell = self.state.level.ghost_home_cells[name]
        self.default_destination_cell = self.state.level.ghost_destination_cells[name]
        self.cell = self.start_cell
        self.direction = self.DEFAULT_DIRECTION
        self.destined_cell = self.default_destination_cell
        self.image = self.get_image(self._get_icon_name())

        self._update_position(self.state.level.get_cell_position(self.cell))

    @classmethod
    def get_image(cls, name):
        if name not in cls.images:
            cls.images[name] = ImageUtils.get(name)

        return cls.images[name]

    def _get_icon_name(self):
        direction_in_lowercase = self.direction.name.lower()

        return f"ghost-{self.name}-{direction_in_lowercase}"