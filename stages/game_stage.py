import os.path
import time
import pygame

from cell_map import CellMap
from game_states import GameStates
from level import Level
from managers.ghosts_manager import GhostsManager
from pacman import Pacman
from managers.collectibles_manager import CollectiblesManager
from stages.stage import Stage, StageUpdateType
from game_info import GameInfo
from utils.audio_utils import AudioUtils
from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


class GameStage(Stage):
    BACKGROUND_CORDS = (0, 0)
    BACKGROUND_NAME = "board"
    BACKGROUND_NAME_WHITE = "board-white"
    MIN_LEVEL = 1
    MAX_LEVEL = 1
    PACMAN_DEAD_TIME = 2500
    LEVEL_END_MUSIC_TIME = 2000
    LEVEL_END_FULL_TIME = 4000
    BACKGROUND_UPDATE_TIME = 150
    START_DELAY = 4000

    def __init__(self):
        super().__init__()
        self.level_id = 0
        self.level = None
        self.collectibles = None
        self.ghosts = None
        self.pacman = None
        self.score = 0
        self.state = GameStates.GAME_START
        self.game_info = None
        self.background = FileUtils.get_image(self.BACKGROUND_NAME)
        self.collected = 0
        self.high_score = self._get_high_score()
        self._current_siren_id = None
        self._main_channel = pygame.mixer.Channel(1)
        self._started = False
        self._state_start = None
        self._last_background_update = None

        CellMap.get_instance()

    def start_game(self):
        self.level_id = self.MIN_LEVEL
        self.level = Level(self)
        self.collectibles = CollectiblesManager(self)
        self.pacman = Pacman(self)
        self.ghosts = GhostsManager(self)
        self.game_info = GameInfo(self)
        self.score = 0
        self._started = True
        self._current_siren_id = None
        self._last_background_update = None
        self.update_state(GameStates.GAME_START)

    def add_score(self, score):
        self.score += score

    def update_state(self, state_type):
        self.state = state_type
        self._state_start = time.time()

        if state_type == GameStates.GAME_START:
            pygame.mixer.stop()
            AudioUtils.get_sound(AudioUtils.BEGINNING_SOUND).play()
        elif state_type == GameStates.DEAD or state_type == GameStates.DEAD_END:
            pygame.mixer.stop()
            AudioUtils.get_sound(AudioUtils.DEATH_SOUND).play()
        elif state_type == GameStates.LEVEL_END:
            pygame.mixer.stop()
            AudioUtils.get_sound(AudioUtils.EXTEND).play()
            self._last_background_update = time.time()

    def start_stage(self, update_type):
        if update_type == StageUpdateType.RESTART or not self._started:
            self.save_high_score()
            self.start_game()
        else:
            pygame.mixer.unpause()

    def update(self, events, key_pressed):
        self._handle_escape(events, key_pressed)
        if self.state == GameStates.GAME_START and TimeUtils.time_elapsed(self._state_start) >= self.START_DELAY:
            self.update_state(GameStates.PLAYING)
        elif self.state == GameStates.PLAYING:
            self._update_sound()
            self.collectibles.update()
            self.pacman.update(key_pressed)
            self.ghosts.update()
        elif self.state == GameStates.DEAD and TimeUtils.time_elapsed(self._state_start) >= self.PACMAN_DEAD_TIME:
            self.pacman.lives -= 1
            self.pacman.reset()
            self.ghosts.reset()
            self.update_state(GameStates.GAME_START)
        elif self.state == GameStates.DEAD_END and TimeUtils.time_elapsed(self._state_start) >= self.PACMAN_DEAD_TIME:
            self.notify(StageUpdateType.START_MENU)
        elif self.state == GameStates.LEVEL_END:
            time_elapsed = TimeUtils.time_elapsed(self._state_start)
            if self.LEVEL_END_FULL_TIME > time_elapsed >= self.LEVEL_END_MUSIC_TIME:
                self._animate_background()
            elif time_elapsed >= self.LEVEL_END_FULL_TIME:
                self.background = FileUtils.get_image(self.BACKGROUND_NAME)
                self._next_level()

    def _animate_background(self):
        if TimeUtils.time_elapsed(self._last_background_update) >= self.BACKGROUND_UPDATE_TIME:
            if self.background == FileUtils.get_image(self.BACKGROUND_NAME):
                self.background = FileUtils.get_image(self.BACKGROUND_NAME_WHITE)
            else:
                self.background = FileUtils.get_image(self.BACKGROUND_NAME)
            self._last_background_update = time.time()

    def _next_level(self):
        self.notify(StageUpdateType.START_MENU)

    def _update_sound(self):
        siren_id = self._get_siren_id()
        if not self._main_channel.get_busy() or self._current_siren_id != siren_id:
            self._main_channel.stop()
            self._main_channel.play(AudioUtils.get_sound(AudioUtils.SIRENS[siren_id]), loops=-1)
            self._current_siren_id = siren_id

    def _get_siren_id(self):
        percent_collected = self.collected / CellMap.get_instance().count * 100
        siren_id = None
        if percent_collected < 50:
            siren_id = 0
        else:
            siren_id = 1

        return siren_id

    def _handle_escape(self, events, key_pressed):
        for event in events:
            if key_pressed[pygame.K_ESCAPE]:
                self.notify(StageUpdateType.PAUSE)
                break

    def render(self, screen):
        self._render_background(screen)
        self.collectibles.render(screen)
        self.pacman.render(screen)
        self.game_info.render(screen)

        if self.state != GameStates.LEVEL_END:
            self.ghosts.render(screen)

    def _render_background(self, screen):
        screen.blit(self.background, self.BACKGROUND_CORDS)

    def save_high_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score
            with open(os.path.join(FileUtils.PATH_TO_RESOURCES, 'cache.bin'), 'wb') as file:
                file.write(self.score.to_bytes(24, byteorder='big', signed=False))

    @classmethod
    def _get_high_score(cls):
        try:
            with open(os.path.join(FileUtils.PATH_TO_RESOURCES, 'cache.bin'), 'rb') as file:
                return int.from_bytes(file.read(), byteorder='big')
        except (ValueError, FileNotFoundError):
            return 0
