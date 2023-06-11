import pygame


class Collectible(pygame.sprite.Sprite):
    def __init__(self, image, position, score, cell):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.position = position
        self.cell = cell
        self.score = score
        self.rect = self.image.get_rect(center=position)

    def collect(self, board):
        board.add_score(self.score)
        self.kill()

    def update(self):
        pass

    def collided(self, cell):
        return self.cell == cell
