import os

import pygame


class AudioUtils:
    _loaded = False
    _sounds = {}
    BUTTON_SOUND = "button"
    BEGINNING_SOUND = "game_start"
    DEATH_SOUND = "death"
    EAT_SOUND = "eat_dot"
    EAT_FRUIT_SOUND = "eat_fruit"
    EAT_GHOST_SOUND = "eat_ghost"
    INTERMISSION_SOUND = "intermission"
    EXTEND = "extend"
    POWER_PELLET = "power_pellet"
    SIRENS = ["siren_1", "siren_2", "siren_3", "siren_4", "siren_5"]

    EXTENSION = "wav"
    PATH = os.path.join(os.getcwd(), 'resources', 'sounds')

    ALL_SOUNDS = [BEGINNING_SOUND, DEATH_SOUND, EAT_SOUND, BUTTON_SOUND, EXTEND,
                  EAT_FRUIT_SOUND, EAT_GHOST_SOUND, INTERMISSION_SOUND, POWER_PELLET, *SIRENS]

    @classmethod
    def load_sounds(cls):
        pygame.mixer.init()
        if not cls._loaded:
            for sound in cls.ALL_SOUNDS:
                cls._sounds[sound] = pygame.mixer.Sound(os.path.join(cls.PATH, f"{sound}.{cls.EXTENSION}"))
                cls._sounds[sound].set_volume(0.2)

    @classmethod
    def get_sound(cls, name):
        return cls._sounds[name]