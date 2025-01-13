import pygame
from typing import List, Tuple, Optional, Dict, Any
from board import Board
from user_interface import UserInterface
from piece import Piece
from player import FirstPlayer
from dice import Dice
from DataBase.database import Database
from house import House
from constants import *


class Brasopolis:
    def __init__(self) -> None:
        pygame.init()
        self._screen: pygame.Surface = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Banco Imobiliário")
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._running: bool = True
        self._board: Board = Board()
        self._ui: UserInterface = UserInterface(self._screen)
        self._players: List[FirstPlayer] = []
        self._pieces: List[Piece] = []
        self._current_player: int = 0
        self._dice: Dice = Dice((260, 360))
        self._prompt_data: Optional[Dict[str, Any]] = (
            None  # Armazena dados do prompt atual (se houver)
        )
        self._database: Database = Database()

    def run(self) -> None:
        player_count: int = self._ui.show_player_count_selection()
        player_names: List[str] = self._ui.show_login_screen(player_count)
        self._players = [FirstPlayer(name) for name in player_names]
        self._board.load_map()
        self._initialize_pieces()
        self._game_loop()

    def save_records(self) -> None:
        for player in self._players:
            self._database.insert_record(player.name, player.money)
        self._database.close()

    def handle_house_event(self, player: FirstPlayer, house: House) -> None:
        """Gerencia os eventos ao cair em uma casa."""
        if house.owner is None and house.status == "disponível":
            # Jogador pode comprar ou alugar a casa
            self._ui.show_message(f"{player.name}, você caiu na casa {house.name}.")
            choice = self._ui.show_purchase_or_rent_option(house)
            if choice == "comprar":
                if player.money >= house.custom_price:
                    player.money -= house.custom_price
                    house.owner = player
                    house.status = "vendido"
                    self._ui.show_message(f"{player.name} comprou {house.name}.")
                else:
                    self._ui.show_message("Dinheiro insuficiente para a compra.")
            elif choice == "alugar":
                if player.money >= house.custom_price * 0.2:  # 20% do preço para alugar
                    player.money -= house.custom_price * 0.2
                    house.owner = player
                    house.status = "alugado"
                    house.rent_turns_left = 2  # Dura duas voltas completas
                    self._ui.show_message(f"{player.name} alugou {house.name}.")
        elif house.owner and house.owner != player:
            # Pagar aluguel ao proprietário
            rent: float = house.custom_price * 0.05
            if player.money >= rent:
                player.money -= rent
                house.owner.money += rent
                self._ui.show_message(
                    f"{player.name} pagou R$ {rent:.2f} de aluguel para {house.owner.name}."
                )
            else:
                self._ui.show_message(
                    f"{player.name} não tem dinheiro suficiente para pagar o aluguel."
                )
                # Implementar lógica de falência, se necessário
        elif house.custom_gain > 0:
            # Casas de bônus
            player.money += house.custom_gain
            self._ui.show_message(f"{player.name} ganhou R$ {house.custom_gain:.2f}.")
        elif house.custom_loss > 0:
            # Casas de penalidade
            player.money -= house.custom_loss
            self._ui.show_message(f"{player.name} perdeu R$ {house.custom_loss:.2f}.")
        elif house.name in ["Casa de Prisão"]:  # Exemplo para a casa índice 13
            self._ui.show_message(f"{player.name} está preso na casa {house.name}.")
            self._handle_prison(player)

    def _handle_prison(self, player: FirstPlayer) -> None:
        """Gerencia o comportamento de um jogador na prisão."""
        if player.money >= 200000:
            choice = self._ui.show_prison_escape_option()
            if choice == "pagar":
                player.money -= 200000
                self._ui.show_message(f"{player.name} pagou para sair da prisão.")
                return
        dice_value: int = self._dice.roll()
        self._ui.show_message(f"{player.name} tirou {dice_value} no dado.")
        if dice_value == 6:
            self._ui.show_message(f"{player.name} saiu da prisão!")
        else:
            player.skip_turns = 1

    def _move_current_player(self, dice_value: int) -> None:
        """Move o jogador atual no tabuleiro com base no resultado do dado."""
        current_piece: Piece = self._pieces[self._current_player]
        current_index: int = self._board.houses.index(current_piece.current_house)
        next_index: int = (current_index + dice_value) % len(self._board.houses)
        current_house: House = self._board.houses[next_index]
        current_piece.move_to(current_house)

        # Regras para casas especiais
        if next_index in [7, 21]:  # Recebe dinheiro
            self._players[self._current_player].money += 200000
        elif next_index == 12:  # Paga multa
            self._players[self._current_player].money -= 300000
        elif next_index == 35:
            self._players[self._current_player].money -= 100000
        elif next_index == 20 or next_index == 34:  # Perde turnos
            self._players[self._current_player].turns_lost = 2

        # Gerenciar aluguel ou compra
        if current_house.status == "disponível":
            self._prompt_data = {
                "house": current_house,
                "player": self._players[self._current_player],
            }
        elif (
            current_house.is_owned()
            and current_house.owner != self._players[self._current_player]
        ):
            rent: float = current_house.custom_price * 0.05
            self._players[self._current_player].money -= rent
            current_house.owner.money += rent

        # Atualizar status de aluguel expirado
        for house in self._board.houses:
            if house.status == "alugada" and house.rent_turns_left > 0:
                house.rent_turns_left -= 1
            if house.rent_turns_left == 0:
                house.reset_rent()

        # Alternar turno se não houver prompt
        if not self._prompt_data:
            self._switch_turn()

    def _initialize_pieces(self) -> None:
        """Inicializa as peças dos jogadores no tabuleiro."""
        colors: List[Tuple[int, int, int]] = [
            RED,
            PIECE_GREEEN,
            PIECE_BLUE,
            PIECE_YELLOW,
        ]  # Cores das peças
        for i, player in enumerate(self._players):
            initial_house: House = self._board.houses[
                0
            ]  # Casa inicial é a primeira do tabuleiro
            piece: Piece = Piece(
                color=colors[i % len(colors)], initial_house=initial_house
            )
            player.piece = piece
            self._pieces.append(piece)

    def _switch_turn(self) -> None:
        """Alterna o turno entre os jogadores."""
        self._current_player = (self._current_player + 1) % len(self._players)

    def _game_loop(self) -> None:
        while self._running:
            map_rect: pygame.Rect = self._board.get_scaled_map().get_rect(
                center=(self._screen.get_width() // 2, self._screen.get_height() // 2)
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                # Verificar clique no botão do dado
                dice_result: Optional[int] = self._dice.handle_event(event)
                if dice_result and not self._prompt_data:
                    self._move_current_player(dice_result)

                # Tratar eventos do tabuleiro
                self._board.handle_event(event)

                # Tratar eventos de teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:  # Pressionar 'L' para fechar o jogo
                        self._running = False

            # Atualizar e desenhar elementos na tela
            self._screen.fill((0, 0, 0))
            self._board.draw(self._screen)
            self._dice.draw(
                self._screen,
                self._board.interact,
                self._board.zoom,
                (map_rect.left, map_rect.top),
            )
            map_rect = self._board.get_scaled_map().get_rect(
                center=(self._screen.get_width() // 2, self._screen.get_height() // 2)
            )
            for piece in self._pieces:
                piece.draw(
                    self._screen, self._board.zoom, (map_rect.left, map_rect.top)
                )

            self._ui.draw_interface(
                self._screen,
                self._players[self._current_player],
                self._pieces[self._current_player],
                self._board.interact,
                self._board.zoom,
                (map_rect.left, map_rect.top),
            )

            # Exibir prompt, se necessário
            if self._prompt_data:
                action: str = self._ui.prompt_buy_or_rent(
                    self._prompt_data["house"],
                    self._board.interact,
                    self._board.zoom,
                    (map_rect.left, map_rect.top),
                )
                if action == "comprar":
                    self._prompt_data["house"].owner = self._prompt_data["player"]
                    self._prompt_data["house"].status = "comprada"
                    self._prompt_data["player"].money -= self._prompt_data[
                        "house"
                    ].custom_price
                elif action == "alugar":
                    self._prompt_data["house"].owner = self._prompt_data["player"]
                    self._prompt_data["house"].status = "alugada"
                    self._prompt_data["house"].rent_turns_left = 2

                # Limpar o estado do prompt e alternar turno
                self._prompt_data = None
                self._switch_turn()

            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()
