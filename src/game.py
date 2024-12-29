import pygame
from board import Board
from user_interface import UserInterface
from piece import Piece
from player import Player
from dice import Dice


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
        self.pieces = []
        self.current_player = 0
        self.dice = Dice((300, 600))

    def run(self):
        player_count = self.ui.show_player_count_selection()
        player_names = self.ui.show_login_screen(player_count)
        self.players = [Player(name) for name in player_names]
        self.board.load_map()
        self.initialize_pieces()
        self.game_loop()

    def move_current_player(self, dice_value):
        """Move o jogador atual no tabuleiro com base no resultado do dado."""
        current_piece = self.pieces[self.current_player]
        current_index = self.board.houses.index(current_piece.current_house)
        next_index = (current_index + dice_value) % len(self.board.houses)
        current_piece.move_to(self.board.houses[next_index])

        # Alternar turno após o movimento
        self.switch_turn()

    def initialize_pieces(self):
        """Inicializa as peças dos jogadores no tabuleiro."""
        colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
        ]  # Cores das peças
        for i, player in enumerate(self.players):
            initial_house = self.board.houses[
                0
            ]  # Casa inicial é a primeira do tabuleiro
            piece = Piece(color=colors[i % len(colors)], initial_house=initial_house)
            player.piece = piece
            self.pieces.append(piece)

    def switch_turn(self):
        """Alterna o turno entre os jogadores."""
        self.current_player = (self.current_player + 1) % len(self.players)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Verificar clique no botão do dado
                dice_result = self.dice.handle_event(event)
                if dice_result:
                    self.move_current_player(dice_result)

                # Tratar eventos do tabuleiro
                self.board.handle_event(event)

                # Tratar eventos de teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:  # Pressionar 'L' para fechar o jogo
                        self.running = False

            # Desenhar elementos na tela
            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)
            self.dice.draw(self.screen)  # Desenha o botão do dado

            map_rect = self.board.get_scaled_map().get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
            )
            for piece in self.pieces:
                piece.draw(self.screen, self.board.zoom, (map_rect.left, map_rect.top))

            self.ui.draw_interface(
                self.screen,
                self.players[self.current_player],
                self.pieces[self.current_player],
                self.board.interact,
                self.board.zoom,
                (map_rect.left, map_rect.top),
            )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
