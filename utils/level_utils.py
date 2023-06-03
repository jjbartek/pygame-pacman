import json
import os

from level import Level


class LevelUtils:
    MIN_LEVEL = 1
    MAX_LEVEL = 1
    PATH_TO_LEVEL_FILES = os.path.join(os.getcwd(), 'resources', 'levels')
    LEVEL_FILE_EXTENSION = "json"

    CHAR_TO_CELL_TYPE_MAP = {
        "|": "add_wall",
        "-": "add_space",
        "*": "add_dot",
        "&": "add_energizer",
        "+": "add_teleport"
    }

    @classmethod
    def get_level(cls, level_id):
        return cls._from_level_id(level_id)

    @classmethod
    def _from_level_id(cls, level_id):
        level_data = cls._get_level_data(cls._get_level_path(level_id))

        level_id = level_data["id"]
        background_name = level_data["backgroundName"]
        structure = level_data["structure"]
        cells_per_plane = level_data["cellsPerPlane"]
        dimensions_in_pixels = level_data["dimensionsInPixels"]
        cell_size_in_pixels = level_data["cellSizeInPixels"]
        default_cell = level_data["defaultCell"]
        offset = level_data["offset"]

        return Level(level_id, background_name, structure, cells_per_plane, dimensions_in_pixels, cell_size_in_pixels,
                     default_cell, offset)

    @classmethod
    def _get_level_data(cls, path):
        with open(path, 'r') as f:
            level_data = json.load(f)

        return level_data

    @classmethod
    def _get_level_path(cls, level_id):
        return os.path.join(cls.PATH_TO_LEVEL_FILES, cls._get_level_filename(level_id))

    @classmethod
    def _get_level_filename(cls, level_id):
        return f"{level_id}.{cls.LEVEL_FILE_EXTENSION}"
