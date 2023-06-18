import time

import pygame

from enums.game_states import GameState
from enums.ghost_mode import GhostMode
from entities.inky import Inky
from entities.blinky import Blinky
from entities.clyde import Clyde
from entities.pinky import Pinky
from enums.units import Units
from utils.time_utils import TimeUtils


class GhostsManager:
    FRIGHTENED_TIME = 10
    START_ANIMATION_AT_PERCENT = 60
    GHOST_DEAD_FREEZE_TIME = 500
    START_MODE = GhostMode.SCATTER

    # GHOST_LEAVE_TIME

    def __init__(self, game):
        self.game = game
        self.group = pygame.sprite.Group()
        self.current_mode = None
        self.blinky = Blinky(self)
        self.pinky = Pinky(self)
        self.inky = Inky(self)
        self.clyde = Clyde(self)
        self.previous_mode = None
        self.scatter_duration = [1, 1, 1, 1]
        self.chase_duration = [2, 2, 2, None]
        self.fright_duration = self.FRIGHTENED_TIME
        self.current_mode_duration = None
        self._mode_start_time = time.time()
        self._channel = pygame.mixer.Channel(3)
        self._before_pause_elapsed = None
        self._before_frightened_elapsed = None
        self._before_frightened_duration = None
        self._chase_counter = -1
        self._scatter_counter = -1

        self.group.add(self.blinky)
        self.group.add(self.pinky)
        self.group.add(self.inky)
        self.group.add(self.clyde)

        self.update_mode(self.START_MODE)

        self.clyde.activate()
        self.pinky.activate()
        self.inky.activate()
        self.blinky.activate()

    def update(self):
        if self._should_update_mode():
            if self.current_mode == GhostMode.FRIGHTENED:
                next_mode = self.previous_mode
            else:
                next_mode = GhostMode.SCATTER if self.current_mode == GhostMode.CHASE else GhostMode.CHASE
            self.update_mode(next_mode)

        for ghost in self.group:
            ghost.update()

    def _should_update_mode(self):
        return self.current_mode_duration is not None and \
            TimeUtils.elapsed(self._mode_start_time, unit=Units.Seconds) >= self.current_mode_duration

    def update_mode(self, mode):
        self._update_mode_duration_time(mode)
        self._set_previous_mode(mode)
        self._update_mode_start_time(mode)
        self.current_mode = mode

        for ghost in self.group:
            ghost.reset_dead()
            if self.previous_mode != GhostMode.FRIGHTENED and self.previous_mode != self.current_mode:
                ghost.reverse_direction()

    def _update_mode_start_time(self, new_mode):
        if self.current_mode != GhostMode.FRIGHTENED and new_mode == GhostMode.FRIGHTENED:
            self._before_frightened_elapsed = time.time() - self._mode_start_time

        if self.current_mode == GhostMode.FRIGHTENED and new_mode != GhostMode.FRIGHTENED:
            self._mode_start_time = time.time() - self._before_frightened_elapsed
            self._before_frightened_elapsed = None
        else:
            self._mode_start_time = time.time()

    def _update_mode_duration_time(self, new_mode):
        if new_mode == GhostMode.FRIGHTENED:
            if self.current_mode != GhostMode.FRIGHTENED:
                self._before_frightened_duration = self.current_mode_duration
            self.current_mode_duration = self.fright_duration
        elif new_mode == GhostMode.CHASE:
            self.current_mode_duration = self._get_chase_duration()
        elif new_mode == GhostMode.SCATTER:
            self.current_mode_duration = self._get_scatter_duration()

    def _get_chase_duration(self):
        if self.current_mode == GhostMode.FRIGHTENED:
            return self._before_frightened_duration
        else:
            self._chase_counter += 1
            return self.chase_duration[self._chase_counter]

    def _get_scatter_duration(self):
        if self.current_mode == GhostMode.FRIGHTENED:
            return self._before_frightened_duration
        else:
            self._scatter_counter += 1
            return self.scatter_duration[self._scatter_counter]

    def _set_previous_mode(self, mode):
        if self.current_mode != mode:
            self.previous_mode = self.current_mode

    def handle_ghost_dead(self):
        # self.game.add_score()
        self.pause()
        self.game.update_state(GameState.GHOST_DEAD)

    def handle_pacman_dead(self):
        if self.game.pacman.lives > 1:
            self.game.update_state(GameState.DEAD)
        else:
            self.game.update_state(GameState.DEAD_END)

    def render(self, screen):
        for ghost in self.group:
            ghost.render(screen)

    def reset(self):
        if self.current_mode == GhostMode.FRIGHTENED:
            self.current_mode = self.previous_mode
        self._mode_start_time = time.time()
        for ghost in self.group:
            ghost.reset()

        self.clyde.activate()
        self.pinky.activate()
        self.inky.activate()
        self.blinky.activate()

    def should_animate_icon(self):
        mode_finish_percent = TimeUtils.elapsed(self._mode_start_time, unit=Units.Seconds) / self.fright_duration * 100
        return mode_finish_percent >= self.START_ANIMATION_AT_PERCENT

    def pause(self):
        self._before_pause_elapsed = time.time() - self._mode_start_time

    def unpause(self):
        self._mode_start_time = time.time() - self._before_pause_elapsed
        self._before_pause_elapsed = None
