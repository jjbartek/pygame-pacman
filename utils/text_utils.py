import os

import pygame


class TextUtils:
    _fonts = {}
    _texts = {}
    FONT_PATH = os.path.join(os.getcwd(), 'resources', 'emulgic.ttf')

    @classmethod
    def get_text(cls, text, size, color, cache=True):
        if not cache:
            font = cls._get_font(size)
            return font.render(text, True, color)

        key = (text, size, color)
        if key not in cls._texts:
            font = cls._get_font(size)
            cls._texts[key] = font.render(text, True, color)

        return cls._texts[key]

    @classmethod
    def _get_font(cls, size):
        if size not in cls._fonts:
            cls._fonts[size] = pygame.font.Font(cls.FONT_PATH, size)

        return cls._fonts[size]