from level import Level
from utils.file_utils import FileUtils


class LevelManager:
    MIN_LEVEL = 1
    LEVEL_ID_TO_FILE_NAME = {
        (1, 1): "level_1",
        (2, float('inf')): "level_2"
    }

    def __init__(self, game):
        self._current_level_id = None
        self._current_level_name = None
        self.current = None
        self.game = game

        self.set_next_level()

    def set_next_level(self):
        if self._current_level_id is not None:
            self._current_level_id += 1
        else:
            self._current_level_id = self.MIN_LEVEL

        next_level_name = self._get_level_name(self._current_level_id)
        if next_level_name != self._current_level_name:
            self._current_level_name = next_level_name
            self.current = self._from_level_name(next_level_name)

    @classmethod
    def _get_level_name(cls, level_id):
        for level_id_range in cls.LEVEL_ID_TO_FILE_NAME:
            min_level, max_level = level_id_range
            if min_level <= level_id <= max_level:
                return cls.LEVEL_ID_TO_FILE_NAME.get(level_id_range)
        return None

    @classmethod
    def _from_level_name(cls, level_name):
        level_data = FileUtils.get_level_data(level_name)

        chase_duration = level_data["chase_duration"]
        scatter_duration = level_data["scatter_duration"]
        fright_duration = level_data["fright_duration"]
        elroy_1_dots = level_data["elroy_1_dots"]
        elroy_1_speed = level_data["elroy_1_speed"]
        elroy_2_dots = level_data["elroy_2_dots"]
        elroy_2_speed = level_data["elroy_2_speed"]
        pacman_speed_normal = level_data["pacman_speed_normal"]
        pacman_dots_normal = level_data["pacman_dots_normal"]
        pacman_speed_fright = level_data["pacman_speed_fright"]
        pacman_dots_fright = level_data["pacman_dots_fright"]
        ghost_speed_normal = level_data["ghost_speed_normal"]
        ghost_speed_fright = level_data["ghost_speed_fright"]
        ghost_speed_tunnel = level_data["ghost_speed_tunnel"]
        clyde_dots_to_leave = level_data["clyde_dots_to_leave"]
        inky_dots_to_leave = level_data["inky_dots_to_leave"]
        bonus = level_data["bonus"]
        bonus_points = level_data["bonus_points"]

        return Level(chase_duration,
                     scatter_duration,
                     fright_duration,
                     elroy_1_dots,
                     elroy_1_speed,
                     elroy_2_dots,
                     elroy_2_speed,
                     pacman_speed_normal,
                     pacman_dots_normal,
                     pacman_speed_fright,
                     pacman_dots_fright,
                     ghost_speed_normal,
                     ghost_speed_fright,
                     ghost_speed_tunnel,
                     clyde_dots_to_leave,
                     inky_dots_to_leave,
                     bonus,
                     bonus_points)
