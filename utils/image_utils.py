import os
import pygame


class ImageUtils:
    PATH_TO_IMAGES = os.path.join(os.getcwd(), 'resources', 'images')

    @classmethod
    def get(cls, name, extension="png"):
        filename = cls._build_filename(name, extension)
        loaded_image = cls._load(filename)
        converted_image = cls._convert(loaded_image)

        return converted_image

    @staticmethod
    def _load(filename):
        return pygame.image.load(os.path.join(ImageUtils.PATH_TO_IMAGES, filename))

    @staticmethod
    def _convert(image):
        return image.convert_alpha()

    @staticmethod
    def _build_filename(name, extension):
        return f"{name}.{extension}"
