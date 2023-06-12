import pygame

from cell_map import CellMap


class CollectiblesManager:
    def __init__(self, game):
        self.group = pygame.sprite.Group()
        self.game = game

        self._load()

    def render(self, screen):
        self.group.draw(screen)

    def add(self, collectible):
        self.group.add(collectible)

    def update(self):
        for collectible in self.group:
            if collectible.collided(self.game.pacman.cell):
                collectible.collect(self.game)
            elif not self.game.freeze:
                collectible.update()

    def _load(self):
        all_collectibles = CellMap.get_instance().collectibles
        for collectible_type in all_collectibles:
            for cell in all_collectibles[collectible_type]:
                position = CellMap.get_cell_position(cell)
                self.add(collectible_type(position, cell))
