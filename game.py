import os
import pygame
from levels.level1 import Level1


class Game:
    def __init__(self):
        pygame.init()
        self.board_position = None
        self.board_image = None
        self.is_running = True
        self.images_path = os.path.join(os.getcwd(), 'resources', 'images')
        self.sounds_path = os.path.join(os.getcwd(), 'resources', 'sounds')
        self.screen_size = self.width, self.height = 559, 699
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.levels = [Level1]
        self.current_level = self.levels[0]()

        # load game icon and title
        pygame.display.set_caption("PACMAN")
        pygame.display.set_icon(pygame.image.load(os.path.join(self.images_path, "icon.png")))
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[pygame.K_ESCAPE]:
                self.is_running = False

    def load_board(self):
        self.board_image = pygame.image.load(self.current_level.background).convert()
        self.board_position = self.current_level.position

    def show_game(self):
        self.screen.blit(self.board_image, self.board_position)

    def run(self):
        self.load_board()

        while self.is_running:
            self.clock.tick(60)
            self.check_events()
            self.show_game()

            pygame.display.flip()
            pygame.event.pump()  # ?

        pygame.quit()


game = Game()
game.run()
