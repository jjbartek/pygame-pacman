import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, image, position, score, countable, cell):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.position = position
        self.cell = cell
        self.score = score
        self.countable = countable
        self.rect = self.image.get_rect(center=position)

    def update(self):
        pass

    def collided(self, cell):
        return self.cell == cell
