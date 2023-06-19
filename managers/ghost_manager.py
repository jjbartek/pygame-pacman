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


class GhostManager:
    FRIGHTENED_TIME = 10
    START_ANIMATION_AT_PERCENT = 60
    GHOST_DEAD_FREEZE_TIME = 500
    GHOST_DEAD_SCORE = 200
    START_MODE = GhostMode.SCATTER

    def __init__(self, game):
        self.game = game
        self.ghosts = pygame.sprite.Group()
        self.current_mode = None
        self.blinky = Blinky(self)
        self.pinky = Pinky(self)
        self.inky = Inky(self)
        self.clyde = Clyde(self)
        self.previous_mode = None
        self.current_mode_duration = None
        self._mode_start_time = time.time()
        self._channel = pygame.mixer.Channel(3)
        self._before_pause_elapsed = None
        self._before_frightened_elapsed = None
        self._chase_counter = -1
        self._scatter_counter = -1
        self._dots_counter = 0
        self._first_round = True
        self._dead_ghosts_counter = 0

        self._ghosts_to_activate = [self.inky, self.clyde]

        self.ghosts.add(self.blinky)
        self.ghosts.add(self.pinky)
        self.ghosts.add(self.inky)
        self.ghosts.add(self.clyde)

        self.blinky.activate()
        self.pinky.activate()

        self.update_mode(self.START_MODE)

    def update(self):
        if self._should_update_mode():
            if self.current_mode == GhostMode.FRIGHTENED:
                next_mode = self.previous_mode
            else:
                next_mode = GhostMode.SCATTER if self.current_mode == GhostMode.CHASE else GhostMode.CHASE
            self.update_mode(next_mode)

        for ghost in self.ghosts:
            ghost.update()

    def update_counter(self):
        if len(self._ghosts_to_activate) > 0:
            self._dots_counter += 1
            first_ghost = self._ghosts_to_activate[0]
            dots_needed = first_ghost.get_dots_to_leave() if self._first_round else first_ghost.dots_after_death
            if self._dots_counter >= dots_needed:
                first_ghost.activate()
                self._ghosts_to_activate.pop(0)
                self._dots_counter = 0

    def _should_update_mode(self):
        return (self.current_mode_duration is not None
                and TimeUtils.elapsed(self._mode_start_time, unit=Units.Seconds) >= self.current_mode_duration) \
            or self._can_end_frightened()

    def _can_end_frightened(self):
        return self.current_mode == GhostMode.FRIGHTENED and \
            self._dead_ghosts_counter == len(self.ghosts) - len(self._ghosts_to_activate)

    def update_mode(self, mode):
        if self.current_mode == GhostMode.FRIGHTENED:
            self._dead_ghosts_counter = 0

        for ghost in self.ghosts:
            ghost.reset_dead()
            if self.current_mode != GhostMode.FRIGHTENED:
                ghost.reverse_direction()

        self._update_mode_duration_time(mode)
        self._set_previous_mode(mode)
        self._update_mode_start_time(mode)
        self.current_mode = mode

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
            self.current_mode_duration = self.game.levels.current.fright_duration
        elif new_mode == GhostMode.CHASE:
            self.current_mode_duration = self._get_chase_duration()
        elif new_mode == GhostMode.SCATTER:
            self.current_mode_duration = self._get_scatter_duration()

    def _get_chase_duration(self):
        if self.current_mode != GhostMode.FRIGHTENED:
            self._chase_counter += 1

        return self.game.levels.current.chase_duration[self._chase_counter]

    def _get_scatter_duration(self):
        if self.current_mode != GhostMode.FRIGHTENED:
            self._scatter_counter += 1

        return self.game.levels.current.scatter_duration[self._scatter_counter]

    def _set_previous_mode(self, mode):
        if self.current_mode != mode:
            self.previous_mode = self.current_mode

    def handle_ghost_dead(self, ghost):
        self._dead_ghosts_counter += 1
        score = self.GHOST_DEAD_SCORE * (2 ** (self._dead_ghosts_counter - 1))
        ghost.set_dead_text(score)
        self.game.add_score(score)
        self.game.update_state(GameState.EAT_GHOST_FREEZE)

    def handle_pacman_dead(self):
        if self.game.pacman.lives > 1:
            self.game.update_state(GameState.DEAD)
        else:
            self.game.update_state(GameState.DEAD_END)

    def render(self, screen):
        for ghost in self.ghosts:
            ghost.render(screen)

    def reset(self):
        if self.current_mode == GhostMode.FRIGHTENED:
            self._before_frightened_elapsed = 0
            self.update_mode(self.previous_mode)

        self._mode_start_time = time.time()
        for ghost in self.ghosts:
            ghost.reset()

        self._dots_counter = 0
        self._ghosts_to_activate = [self.inky, self.clyde]
        self.blinky.activate()
        self.pinky.activate()
        self._first_round = False

    def reset_timer(self):
        self._mode_start_time = time.time()

    def should_animate_icon(self):
        finish_percent = TimeUtils.elapsed(self._mode_start_time, unit=Units.Seconds) / self.current_mode_duration * 100
        return finish_percent >= self.START_ANIMATION_AT_PERCENT

    def pause(self):
        self._before_pause_elapsed = time.time() - self._mode_start_time

    def unpause(self):
        self._mode_start_time = time.time() - self._before_pause_elapsed
        self._before_pause_elapsed = None
