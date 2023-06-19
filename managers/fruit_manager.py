import pygame

from cell_map import CellMap
from enums.game_states import GameState
from utils.audio_utils import AudioUtils


class FruitManager:
    FRUITS_PER_LEVEL = 2
    ADD_FRUIT_WHEN_COLLECTED = [70, 170]
    FRUIT_CELL = (13.5, 20)

    def __init__(self, game):
        self.fruits = pygame.sprite.Group()
        self.game = game
        self._eat_channel = pygame.mixer.Channel(3)
        self._fruit_count = 0
        self._fruit_to_remove = None

    def render(self, screen):
        for fruit in self.fruits:
            fruit.render(screen)

    def add(self, collectible):
        self.fruits.add(collectible)

    def update(self):
        if self._fruit_to_remove is not None:
            self._fruit_to_remove.kill()
            self._fruit_to_remove = None

        if self._fruit_count < self.FRUITS_PER_LEVEL:
            collected = self.game.collectibles.collected
            if collected >= self.ADD_FRUIT_WHEN_COLLECTED[self._fruit_count]:
                position = CellMap.get_cell_position(self.FRUIT_CELL)
                new_fruit = self.game.levels.current.fruits[self._fruit_count - 1](position, self.FRUIT_CELL)
                self.fruits.add(new_fruit)
                self._fruit_count += 1

        for fruit in self.fruits:
            fruit.update()

    def handle_collision(self):
        for fruit in self.fruits:
            if fruit.collides(self.game.pacman.rect.center):
                score = self.game.levels.current.fruit_points[self._fruit_count-1]
                self.game.add_score(score)
                fruit.set_text(score)
                self._fruit_to_remove = fruit
                self.game.update_state(GameState.EAT_FRUIT_FREEZE)

    def reset(self):
        for fruit in self.fruits:
            fruit.kill()