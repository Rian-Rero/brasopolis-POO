import pygame
from board import Board
from user_interface import UserInterface


class Brasopolis:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Banco Imobiliário")
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board()
        self.ui = UserInterface(self.screen)
        self.players = []

    def run(self):
        player_count = self.ui.show_player_count_selection()
        self.players = self.ui.show_login_screen(player_count)
        self.board.load_map()
        self.game_loop()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.board.handle_event(event)

            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
