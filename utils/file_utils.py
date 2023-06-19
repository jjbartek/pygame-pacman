import json
import os
import pygame


class FileUtils:
    PATH_TO_RESOURCES = os.path.join(os.getcwd(), 'resources')
    PATH_TO_IMAGES = os.path.join(PATH_TO_RESOURCES, 'images')
    PATH_TO_LEVEL_FILES = os.path.join(PATH_TO_RESOURCES, 'levels')
    STRUCTURE_FILE_NAME = "structure.txt"
    images = {}

    @classmethod
    def get_image(cls, name, extension="png"):
        if name not in cls.images:
            filename = cls._build_filename(name, extension)
            loaded_image = cls._load(filename)
            converted_image = loaded_image.convert_alpha()

            cls.images[name] = converted_image
            return converted_image

        return cls.images[name]

    @staticmethod
    def _load(filename):
        return pygame.image.load(os.path.join(FileUtils.PATH_TO_IMAGES, filename))

    @staticmethod
    def _build_filename(name, extension):
        return f"{name}.{extension}"

    @classmethod
    def get_structure(cls):
        with open(os.path.join(cls.PATH_TO_RESOURCES, cls.STRUCTURE_FILE_NAME), 'r') as f:
            structure = f.read()

        return structure

    @classmethod
    def get_level_data(cls, level_name):
        with open(os.path.join(cls.PATH_TO_LEVEL_FILES, f"{level_name}.json"), 'r') as f:
            level_data = json.load(f)

        return level_data
