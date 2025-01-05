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
        self.dice = Dice((260, 360))
        self.prompt_data = None  # Armazena dados do prompt atual (se houver)

    def run(self):
        player_count = self.ui.show_player_count_selection()
        player_names = self.ui.show_login_screen(player_count)
        self.players = [Player(name) for name in player_names]
        self.board.load_map()
        self.initialize_pieces()
        self.game_loop()

    def handle_house_event(self, player, house):
        """Gerencia os eventos ao cair em uma casa."""
        if house.owner is None and house.status == "disponível":
            # Jogador pode comprar ou alugar a casa
            self.ui.show_message(f"{player.name}, você caiu na casa {house.name}.")
            choice = self.ui.show_purchase_or_rent_option(house)
            if choice == "comprar":
                if player.money >= house.custom_price:
                    player.money -= house.custom_price
                    house.owner = player
                    house.status = "vendido"
                    self.ui.show_message(f"{player.name} comprou {house.name}.")
            elif choice == "alugar":
                if player.money >= house.custom_price * 0.2:  # 20% do preço para alugar
                    player.money -= house.custom_price * 0.2
                    house.owner = player
                    house.status = "alugado"
                    house.rent_turns = 2  # Dura duas voltas completas
                    self.ui.show_message(f"{player.name} alugou {house.name}.")
        elif house.owner and house.owner != player:
            # Pagar aluguel ao proprietário
            rent = house.custom_price * 0.05
            if player.money >= rent:
                player.money -= rent
                house.owner.money += rent
                self.ui.show_message(
                    f"{player.name} pagou R$ {rent:.2f} de aluguel para {house.owner.name}."
                )
            else:
                self.ui.show_message(
                    f"{player.name} não tem dinheiro suficiente para pagar o aluguel."
                )
                # Implementar lógica de falência, se necessário
        elif house.custom_gain > 0:
            # Casas de bônus
            player.money += house.custom_gain
            self.ui.show_message(f"{player.name} ganhou R$ {house.custom_gain:.2f}.")
        elif house.custom_loss > 0:
            # Casas de penalidade
            player.money -= house.custom_loss
            self.ui.show_message(f"{player.name} perdeu R$ {house.custom_loss:.2f}.")
        elif house.name in ["Casa de Prisão"]:  # Exemplo para a casa índice 13
            self.ui.show_message(f"{player.name} está preso na casa {house.name}.")
            self.handle_prison(player)

    def handle_prison(self, player):
        """Gerencia o comportamento de um jogador na prisão."""
        if player.money >= 200000:
            choice = self.ui.show_prison_escape_option()
            if choice == "pagar":
                player.money -= 200000
                self.ui.show_message(f"{player.name} pagou para sair da prisão.")
                return
        dice_value = self.dice.roll()
        self.ui.show_message(f"{player.name} tirou {dice_value} no dado.")
        if dice_value == 6:
            self.ui.show_message(f"{player.name} saiu da prisão!")
        else:
            player.skip_turns = 1

    def move_current_player(self, dice_value):
        """Move o jogador atual no tabuleiro com base no resultado do dado."""
        current_piece = self.pieces[self.current_player]
        current_index = self.board.houses.index(current_piece.current_house)
        next_index = (current_index + dice_value) % len(self.board.houses)
        current_house = self.board.houses[next_index]
        current_piece.move_to(current_house)

        # Gerenciar aluguel ou compra
        if current_house.status == "disponível":
            self.prompt_data = {
                "house": current_house,
                "player": self.players[self.current_player],
            }
        elif (
            current_house.is_owned()
            and current_house.owner != self.players[self.current_player]
        ):
            rent = current_house.custom_price * 0.05
            self.players[self.current_player].money -= rent
            current_house.owner.money += rent

        # Atualizar status de aluguel expirado
        for house in self.board.houses:
            if house.status == "alugada" and house.rent_turns_left > 0:
                house.rent_turns_left -= 1
            if house.rent_turns_left == 0:
                house.reset_rent()

        # Alternar turno se não houver prompt
        if not self.prompt_data:
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
        map_rect = self.board.get_scaled_map().get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Verificar clique no botão do dado
                dice_result = self.dice.handle_event(event)
                if dice_result and not self.prompt_data:
                    self.move_current_player(dice_result)

                # Tratar eventos do tabuleiro
                self.board.handle_event(event)

                # Tratar eventos de teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:  # Pressionar 'L' para fechar o jogo
                        self.running = False

            # Atualizar e desenhar elementos na tela
            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)
            self.dice.draw(
                self.screen,
                self.board.interact,
                self.board.zoom,
                (map_rect.left, map_rect.top),
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

            # Exibir prompt, se necessário
            if self.prompt_data:
                action = self.ui.prompt_buy_or_rent(
                    self.prompt_data["house"],
                    self.board.interact,
                    self.board.zoom,
                    (map_rect.left, map_rect.top),
                )
                if action == "comprar":
                    self.prompt_data["house"].owner = self.prompt_data["player"]
                    self.prompt_data["house"].status = "comprada"
                    self.prompt_data["player"].money -= self.prompt_data[
                        "house"
                    ].custom_price
                elif action == "alugar":
                    self.prompt_data["house"].owner = self.prompt_data["player"]
                    self.prompt_data["house"].status = "alugada"
                    self.prompt_data["house"].rent_turns_left = 2

                # Limpar o estado do prompt e alternar turno
                self.prompt_data = None
                self.switch_turn()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
