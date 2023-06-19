import pygame

from cell_map import CellMap
from enums.game_states import GameState
from utils.audio_utils import AudioUtils


class CollectibleManager:
    def __init__(self, game):
        self.group = pygame.sprite.Group()
        self.game = game
        self._eat_channel = pygame.mixer.Channel(2)
        self.collected = 0

        self._load()

    def render(self, screen):
        self.group.draw(screen)

    def add(self, collectible):
        self.group.add(collectible)

    def update(self):
        for collectible in self.group:
            collectible.update()

    def handle_collision(self, cell):
        collision = False
        for collectible in self.group:
            if collectible.collides(cell):
                if not self._eat_channel.get_sound():
                    self._eat_channel.play(AudioUtils.get_sound(AudioUtils.EAT_SOUND), loops=-1)

                collision = True
                self.game.add_score(collectible.score)
                self.add_collected()
                collectible.on_collect(self.game)
                collectible.kill()

        self.game.pacman.is_eating = collision
        if not collision:
            self._eat_channel.stop()

    def add_collected(self):
        self.collected += 1
        if self.collected >= CellMap.get_instance().count:
            self.game.update_state(GameState.LEVEL_END)
        else:
            self.game.ghosts.update_counter()

    def _load(self):
        all_collectibles = CellMap.get_instance().collectibles
        for collectible_type in all_collectibles:
            for cell in all_collectibles[collectible_type]:
                position = CellMap.get_cell_position(cell)
                self.add(collectible_type(position, cell))
