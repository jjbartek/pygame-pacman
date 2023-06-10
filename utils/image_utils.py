import os
import pygame


class ImageUtils:
    PATH_TO_IMAGES = os.path.join(os.getcwd(), 'resources', 'images')
    images = {}

    @classmethod
    def get(cls, name, extension="png"):
        if name not in cls.images:
            filename = cls._build_filename(name, extension)
            loaded_image = cls._load(filename)
            converted_image = loaded_image.convert_alpha()

            cls.images[name] = converted_image
            return converted_image

        return cls.images[name]

    @staticmethod
    def _load(filename):
        return pygame.image.load(os.path.join(ImageUtils.PATH_TO_IMAGES, filename))

    @staticmethod
    def _build_filename(name, extension):
        return f"{name}.{extension}"
