import json
import os

from level import Level


class LevelUtils:
    MIN_LEVEL = 1
    MAX_LEVEL = 1
    PATH_TO_LEVEL_FILES = os.path.join(os.getcwd(), 'resources', 'levels')
    LEVEL_FILE_EXTENSION = "json"

    @classmethod
    def get_level(cls, level_id):
        return cls._from_level_id(level_id)

    @classmethod
    def _from_level_id(cls, level_id):
        level_data = cls._get_level_data(cls._get_level_path(level_id))

        background_name = level_data["backgroundName"]
        dimensions_in_pixels = level_data["dimensionsInPixels"]
        structure = level_data["structure"]
        cells_per_plane = level_data["cellsPerPlane"]
        pacman_start_cell = level_data["pacmanStartCell"]
        cell_size_in_pixels = level_data["cellSizeInPixels"]
        ghost_home_cells = level_data["ghostHomeCells"]
        ghost_destination_cells = level_data["ghostDestinationCells"]
        ghost_start_cell = level_data["ghostStartCell"]

        return Level(background_name, dimensions_in_pixels, structure, cells_per_plane, cell_size_in_pixels,
                     pacman_start_cell, ghost_home_cells, ghost_destination_cells, ghost_start_cell)

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
