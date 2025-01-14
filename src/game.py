import pygame
from typing import List, Tuple, Optional, Dict, Any
from board import Board
from user_interface import UserInterface
from piece import Piece
from player import FirstPlayer
from dice import Dice
from database import Database
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
        # self._database.close()

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
        elif next_index == 13:  # Jogador está preso
            self._players[self._current_player].is_jailed = True
            self._players[self._current_player].turns_lost = 0  # Enquanto preso

        # Gerenciar aluguel ou compra
        if current_house.status == "Disponivel" or current_house.status == "Comprada":
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
            map_rect = self._board.get_scaled_map().get_rect(
                center=(self._screen.get_width() // 2, self._screen.get_height() // 2)
            )
            if self._players[self._current_player].is_jailed:
                action = self._ui.prompt_jail_action(
                    self._screen,
                    self._players[self._current_player],
                    self._board.interact,
                    self._board.zoom,
                    (map_rect.left, map_rect.top),
                )
                if action == "roll":  # Tentar tirar 6 no dado
                    dice_result = self._dice.roll()
                    if dice_result == 6:
                        self._players[self._current_player].is_jailed = False
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            "Você tirou 6 e saiu da prisão!",
                        )
                    else:
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            f"Você tirou {dice_result}. Ainda está preso!",
                        )
                        self._switch_turn()
                        continue

                elif action == "pay":  # Pagar 200.000 para sair
                    if self._players[self._current_player].money >= 200000:
                        self._players[self._current_player].money -= 200000
                        self._players[self._current_player].is_jailed = False
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            "Você pagou 200.000 e saiu da prisão!",
                        )
                    else:
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            "Você não tem dinheiro suficiente para pagar a fiança!",
                        )
                        self._switch_turn()
                        continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                # Verificar clique no botão do dado
                dice_result: Optional[int] = self._dice.handle_event(event)
                if dice_result and not self._prompt_data:
                    self._move_current_player(13)

                # Tratar eventos do tabuleiro
                self._board.handle_event(event)

                # Tratar eventos de teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:  # Pressionar 'L' para fechar o jogo
                        self.save_records()
                        self._running = False
                    if event.key == pygame.K_o:
                        print(self._database.get_all_records())
                        print(self._database.show_the_records())

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
                self._current_player,
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
                    if self._prompt_data["house"].status == "Disponivel":
                        house_price = self._prompt_data["house"].custom_price
                        if self._prompt_data["player"].money >= house_price:
                            self._prompt_data["house"].owner = self._prompt_data[
                                "player"
                            ]
                            self._prompt_data["house"].status = "Comprada"
                            self._prompt_data["player"].money -= house_price
                            self._prompt_data = None  # Permite trocar de turno
                            self._switch_turn()
                        else:
                            self._ui.displayAlert(
                                self._board.interact,
                                self._board.zoom,
                                (map_rect.left, map_rect.top),
                                "Você não tem dinheiro suficiente para comprar esta propriedade!",
                            )
                    else:
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            "A propriedade já foi comprada!",
                        )

                elif action == "alugar":
                    if (
                        self._prompt_data["house"].owner
                        and self._prompt_data["house"].owner
                        != self._prompt_data["player"]
                    ):
                        rent_cost = self._prompt_data["house"].custom_price * 0.05
                        if self._prompt_data["player"].money >= rent_cost:
                            self._prompt_data["player"].money -= rent_cost
                            self._prompt_data["house"].owner.money += rent_cost
                            self._prompt_data = None  # Permite trocar de turno
                            self._switch_turn()
                        else:
                            self._ui.displayAlert(
                                self._board.interact,
                                self._board.zoom,
                                (map_rect.left, map_rect.top),
                                "Você não tem dinheiro suficiente para pagar o aluguel!",
                            )
                    else:
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            "A propriedade não está disponível para aluguel!",
                        )

                elif action == "vender":
                    if self._prompt_data["house"].owner == self._prompt_data["player"]:
                        self._prompt_data["house"].owner = None
                        self._prompt_data["house"].status = "Disponivel"
                        self._prompt_data = None  # Permite trocar de turno
                        self._switch_turn()
                    else:
                        self._ui.displayAlert(
                            self._board.interact,
                            self._board.zoom,
                            (map_rect.left, map_rect.top),
                            "Você não é o dono desta propriedade!",
                        )

            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()
