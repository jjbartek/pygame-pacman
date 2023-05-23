import pygame
import os
import time

from direction import Direction


class Pacman(pygame.sprite.Sprite):
    icons = {}
    for icon in ["pacman-dead", "pacman-half-down", "pacman-half-left", "pacman-half-up", "pacman-half-right",
                 "pacman-open-down", "pacman-open-left", "pacman-open-up", "pacman-open-right",
                 "pacman-third-down", "pacman-third-left", "pacman-third-up", "pacman-third-right",
                 "pacman-whole-down", "pacman-whole-left", "pacman-whole-up", "pacman-whole-right"]:
        icons[icon] = pygame.image.load(os.path.join('resources', 'images', icon + ".png"))

    def __init__(self, board):
        pygame.sprite.Sprite.__init__(self)

        self.active = False
        self.image = Pacman.icons.get("pacman-whole-up")
        self.board = board
        self.position = board.calculate_position((12.5, 22))
        self.direction = Direction.UP
        self.rect = self.image.get_rect(center=self.position)
        self._icon_counter = 0
        self._last_pacman_update = time.time()

    def show(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, keys):
        direction_mapping = {
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN
        }

        for key in direction_mapping:
            if keys[key]:
                self.direction = direction_mapping.get(key)
                if not self.active:
                    self.active = True
                    self._update_icon()
                    self._last_pacman_update = time.time()
                break
        else:
            time_elapsed = time.time() - self._last_pacman_update
            if time_elapsed >= 0.1:
                self._update_icon()
                self._last_pacman_update = time.time()

        self._move()

    def _update_icon(self):
        self._icon_counter = (self._icon_counter + 1) % 2

        icon_type = "whole" if self._icon_counter == 1 else "open"
        self.image = Pacman.icons.get(f"pacman-{icon_type}-{self.direction.name.lower()}")

    def _move(self):
        pass