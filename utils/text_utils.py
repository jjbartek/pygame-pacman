import os

import pygame


class TextUtils:
    _fonts = {}
    _texts = {}
    SCORE_SIZE = 22
    SCORE_COLOR = (0, 255, 220)
    FONT_PATH = os.path.join(os.getcwd(), 'resources', 'emulgic.ttf')

    @classmethod
    def get_standard_text(cls, text, size, color, cache=True):
        if not cache:
            font = cls._get_font(size)
            return font.render(text, True, color)

        key = (text, size, color)
        if key not in cls._texts:
            font = cls._get_font(size)
            cls._texts[key] = font.render(text, True, color)

        return cls._texts[key]

    @classmethod
    def get_score_text(cls, score):
        text = str(score)
        size = cls.SCORE_SIZE
        color = cls.SCORE_COLOR
        font = pygame.font.SysFont('Helvetica', size)
        return font.render(text, True, color)

    @classmethod
    def _get_font(cls, size):
        if size not in cls._fonts:
            cls._fonts[size] = pygame.font.Font(cls.FONT_PATH, size)

        return cls._fonts[size]