import os
import pygame
from levels.level1 import Level1
from board import Board


class Game:
    def __init__(self):
        pygame.init()
        self.board = None
        self.is_running = True
        self.screen_size = self.width, self.height = 559, 699
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.levels = [Level1]
        self.current_level = self.levels[0]()
        self._level_counter = 0

        # load game icon and title
        pygame.display.set_caption("PACMAN")
        pygame.display.set_icon(pygame.image.load(os.path.join("resources", "images", "icon.png")))
        pygame.display.flip()

    def run(self):
        self._load_board()

        while self.is_running:
            self.clock.tick(60)
            self.board.show()

            events = pygame.event.get()
            self._update(events)
            self.board.update(events)

            pygame.display.flip()
            pygame.event.pump()  # ?

        pygame.quit()

    def _update(self, events):
        for event in events:
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[pygame.K_ESCAPE]:
                self.is_running = False

    def _load_board(self):
        board_image = pygame.image.load(self.current_level.background).convert()
        board_position = self.current_level.position

        with open(self.current_level.structure) as f:
            board_structure = f.readlines()
        self.board = Board(board_image, board_position, board_structure, self.current_level.square_size, self.screen)


game = Game()
game.run()
