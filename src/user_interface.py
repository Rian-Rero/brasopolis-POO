import pygame
from constants import *
from typing import Optional, List, Tuple, Dict, Any


class UserInterface:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.font.Font = pygame.font.Font(None, 50)
        self.small_font: pygame.font.Font = pygame.font.Font(None, 35)
        self.custom_font: pygame.font.Font = pygame.font.Font(None, 30)
        self.users_file: str = "src/DataBase/users.txt"

    def show_player_count_selection(self) -> int:
        """Exibe uma tela para o jogador selecionar a quantidade de jogadores."""
        running: bool = True
        selected_count: Optional[int] = None
        while running:
            self.screen.fill((45, 86, 80))
            self.draw_text(
                "Selecione o número de jogadores (2 a 4):",
                self.screen.get_width() // 2,
                100,
                color=WHITE,
            )

            # Botões para 2, 3 ou 4 jogadores
            screen_width, screen_height = self.screen.get_size()
            button_width, button_height = screen_width // 6, screen_height // 12

            buttons: Dict[str, pygame.Rect] = {
                "2": pygame.Rect(
                    (screen_width - button_width) // 2,
                    screen_height // 3,
                    button_width,
                    button_height,
                ),
                "3": pygame.Rect(
                    (screen_width - button_width) // 2,
                    screen_height // 3 + button_height + 20,
                    button_width,
                    button_height,
                ),
                "4": pygame.Rect(
                    (screen_width - button_width) // 2,
                    screen_height // 3 + 2 * (button_height + 20),
                    button_width,
                    button_height,
                ),
            }

            # Desenhar botões
            for label, rect in buttons.items():
                pygame.draw.rect(self.screen, (111, 185, 174), rect)
                # Desenhar texto sobre o botão
                self.draw_text(
                    label,
                    rect.centerx,
                    rect.centery,
                    font=self.small_font,
                    color=(255, 255, 255),
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for label, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            selected_count = int(label)
                            running = False

        return selected_count

    def show_login_screen(self, player_count: int) -> List[str]:
        """Exibe a tela de login/cadastro para o número de jogadores."""
        players: List[str] = []
        for i in range(1, player_count + 1):
            running: bool = True
            username: str = ""
            while running:
                self.screen.fill((45, 86, 80))
                self.draw_text(
                    f"Jogador {i}: Digite seu nome:",
                    self.screen.get_width() // 2,
                    100,
                    color=WHITE,
                )

                # Campo de texto
                input_box_width, input_box_height = 400, 50
                input_box: pygame.Rect = pygame.Rect(
                    (self.screen.get_width() - input_box_width) // 2,
                    (self.screen.get_height() - input_box_height) // 3,
                    input_box_width,
                    input_box_height,
                )
                pygame.draw.rect(self.screen, (255, 255, 255), input_box)
                self.draw_text(
                    username, input_box.x + 200, input_box.y + 25, font=self.small_font
                )

                # Botão de confirmar
                confirm_button_width, confirm_button_height = 200, 50
                confirm_button: pygame.Rect = pygame.Rect(
                    (self.screen.get_width() - confirm_button_width) // 2,
                    input_box.bottom + 20,
                    confirm_button_width,
                    confirm_button_height,
                )
                pygame.draw.rect(self.screen, (111, 185, 174), confirm_button)
                self.draw_text(
                    "Confirmar",
                    confirm_button.centerx,
                    confirm_button.centery,
                    font=self.small_font,
                    color=(255, 255, 255),
                )

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif event.key == pygame.K_RETURN:
                            if username:
                                players.append(username)
                                running = False
                        else:
                            username += event.unicode
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if confirm_button.collidepoint(event.pos) and username:
                            players.append(username)
                            running = False

        return players

    def prompt_buy_or_rent(
        self, house: Any, interact: List[Any], zoom: float, offset: Tuple[int, int]
    ) -> str:
        """Exibe uma janela perguntando ao jogador se deseja comprar ou alugar a casa."""
        running: bool = True
        font_size: int = round(85 * zoom)
        font: pygame.font.Font = pygame.font.Font(None, font_size)
        clock: pygame.time.Clock = pygame.time.Clock()

        while running:
            acao_button_interact: Any = next(
                (i for i in interact if i.custom_name == "Acao"), None
            )
            font_roboto_light = pygame.font.Font(
                "src/assets/fonts/Roboto.ttf", round(52 * zoom)
            )
            self.draw_text(
                f"A casa '{house.custom_name}' custa R${house.custom_price}.",
                (acao_button_interact.x * zoom + offset[0]) * 1.32,
                (acao_button_interact.y * zoom + offset[1]) * 1.1,
                font=font_roboto_light,
                color=BLACK,
            )
            # Botões
            buy_button_interact: Any = next(
                (i for i in interact if i.custom_name == "Comprar"), None
            )
            rent_button_interact: Any = next(
                (i for i in interact if i.custom_name == "AluguelBotao"), None
            )
            sell_button_interact: Any = next(
                (i for i in interact if i.custom_name == "Vender"), None
            )
            skip_button_interact: Any = next(
                (i for i in interact if i.custom_name == "Pular"), None
            )

            buy_button: pygame.Rect = pygame.Rect(
                (buy_button_interact.x * zoom + offset[0]),
                (buy_button_interact.y * zoom + offset[1]),
                buy_button_interact.width * zoom,
                buy_button_interact.height * zoom,
            )
            rent_button: pygame.Rect = pygame.Rect(
                (rent_button_interact.x * zoom + offset[0]),
                (rent_button_interact.y * zoom + offset[1]),
                rent_button_interact.width * zoom,
                rent_button_interact.height * zoom,
            )
            sell_button: pygame.Rect = pygame.Rect(
                (sell_button_interact.x * zoom + offset[0]),
                (sell_button_interact.y * zoom + offset[1]),
                sell_button_interact.width * zoom,
                sell_button_interact.height * zoom,
            )
            skip_button: pygame.Rect = pygame.Rect(
                (skip_button_interact.x * zoom + offset[0]),
                (skip_button_interact.y * zoom + offset[1]),
                skip_button_interact.width * zoom,
                skip_button_interact.height * zoom,
            )

            # Desenhar botões
            pygame.draw.rect(self.screen, RENT_BUTTON, rent_button, border_radius=15)
            pygame.draw.rect(self.screen, BUY_BUTTON, buy_button, border_radius=15)
            pygame.draw.rect(self.screen, SELL_BUTTON, skip_button, border_radius=15)
            pygame.draw.rect(self.screen, SELL_BUTTON, sell_button, border_radius=15)

            self.draw_text(
                "Comprar",
                buy_button.centerx,
                buy_button.centery,
                font=font,
                color=WHITE,
            )
            self.draw_text(
                "Alugar",
                rent_button.centerx,
                rent_button.centery,
                font=font,
                color=BLACK,
            )
            self.draw_text(
                "Pular",
                skip_button.centerx,
                skip_button.centery,
                font=font,
                color=WHITE,
            )
            self.draw_text(
                "Vender",
                sell_button.centerx,
                sell_button.centery,
                font=font,
                color=WHITE,
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buy_button.collidepoint(event.pos):
                        return "comprar"
                    elif rent_button.collidepoint(event.pos):
                        return "alugar"
                    elif skip_button.collidepoint(event.pos):
                        return "nenhuma"
                    elif sell_button.collidepoint(event.pos):
                        return "vender"

            clock.tick(30)

    def draw_text(
        self,
        text: str,
        x: int,
        y: int,
        font: Optional[pygame.font.Font] = None,
        color: Tuple[int, int, int] = BLACK,
    ) -> None:
        """Desenha texto na tela."""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_text_simple(
        self,
        text: str,
        x: int,
        y: int,
        font: Optional[pygame.font.Font] = None,
        color: Tuple[int, int, int] = BLACK,
    ) -> None:
        """Desenha texto na tela nas coordenadas fornecidas."""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        # A posição será diretamente nas coordenadas (x, y)
        self.screen.blit(text_surface, (x, y))

    def displayAlert(
        self,
        interact: List[Any],
        zoom: float,
        offset: Tuple[int, int],
        text: str,
    ):
        acao_button_interact: Any = next(
            (i for i in interact if i.custom_name == "Acao"), None
        )
        font_roboto_light = pygame.font.Font(
            "src/assets/fonts/Roboto.ttf", round(50 * zoom)
        )

        # Renderiza o texto em uma superfície
        text_surface = font_roboto_light.render(text, True, BLACK)
        text_width, text_height = text_surface.get_size()

        # Define as dimensões e posição do fundo vermelho
        background_rect = pygame.Rect(
            (acao_button_interact.x * zoom + offset[0]) * 0.9,  # Margem esquerda
            (acao_button_interact.y * zoom + offset[1]) * 0.905,  # Margem superior
            acao_button_interact.width
            * zoom
            * 1.3,  # Largura do texto + margens laterais
            acao_button_interact.height
            * zoom
            * 2.9,  # Altura do texto + margens superior e inferior
        )

        # Registra o tempo inicial
        start_time = pygame.time.get_ticks()

        # Loop para exibir por 3 segundos
        while True:
            current_time = pygame.time.get_ticks()
            if current_time - start_time > 1500:  # 3 segundos em milissegundos
                break

            # Desenha o fundo vermelho
            pygame.draw.rect(self.screen, BACKGROUND2, background_rect)

            # Desenha o texto
            self.draw_text(
                f"{text}",
                (acao_button_interact.x * zoom + offset[0]) * 1.30,
                (acao_button_interact.y * zoom + offset[1]) * 1.1,
                font=font_roboto_light,
                color=BLACK,
            )

            pygame.display.flip()  # Atualiza o display

        # Opcional: faça algo depois que o alerta desaparecer

    def draw_interface(
        self,
        screen: pygame.Surface,
        current_player: Any,
        current_piece: Any,
        interact: List[Any],
        zoom: float,
        current_player_index: int,
        offset: Tuple[int, int],
    ) -> None:
        """Exibe informações sobre o jogador atual e outras estatísticas do jogo."""
        # Atualizar a lógica para o jogador atual corretamente
        screen_width: int = screen.get_width()
        player_interact: Any = next(
            (i for i in interact if i.custom_name == "Player"), None
        )
        saldo_interact: Any = next(
            (i for i in interact if i.custom_name == "Saldo"), None
        )
        cidade_interact: Any = next(
            (i for i in interact if i.custom_name == "Cidade"), None
        )
        carta_interact: Any = next(
            (i for i in interact if i.custom_name == "Carta"), None
        )
        proprietario_interact: Any = next(
            (i for i in interact if i.custom_name == "Proprietario"), None
        )
        status_interact: Any = next(
            (i for i in interact if i.custom_name == "Status"), None
        )
        aluguel_interact: Any = next(
            (i for i in interact if i.custom_name == "Aluguel"), None
        )

        inputs_font = pygame.font.Font(None, round(95 * zoom))

        # Nome do jogador atual
        self.draw_text(
            f"{current_player.name}",
            (player_interact.x * zoom + offset[0]) * 1.45,
            (player_interact.y * zoom + offset[1]) * 1.05,
            font=inputs_font,
            color=BLACK,
        )
        # Mostrar saldo do jogador atual
        self.draw_text(
            f"{current_player.money:.2f}",
            (saldo_interact.x * zoom + offset[0]) * 1.25,
            (saldo_interact.y * zoom + offset[1]) * 1.03,
            font=inputs_font,
            color=BLACK,
        )

        # Mostrar status da casa atual
        self.draw_text(
            f"{current_piece.current_house.status}",
            (status_interact.x * zoom + offset[0]) * 1.1,
            (status_interact.y * zoom + offset[1]) * 1.02,
            font=inputs_font,
            color=BLACK,
        )
        owner = current_piece.current_house.getOwner()

        # Mostrar proprietário da casa atual
        self.draw_text(
            f"{owner}",
            (proprietario_interact.x * zoom + offset[0]) * 1.07,
            (proprietario_interact.y * zoom + offset[1]) * 1.02,
            font=inputs_font,
            color=BLACK,
        )

        # Imagem do jogador atual
        image_map: Dict[str, pygame.Surface] = self.get_image_map(
            (carta_interact.width * zoom, carta_interact.height * zoom)
        )
        image: Optional[pygame.Surface] = image_map.get(
            current_piece.current_house.custom_name
        )
        if image:
            screen.blit(
                image,
                (
                    (carta_interact.x * zoom + offset[0]),
                    (carta_interact.y * zoom + offset[1]),
                ),
            )
        self.draw_text(
            f"{current_piece.current_house.custom_name}",
            (cidade_interact.x * zoom + offset[0]) * 1.1,
            (cidade_interact.y * zoom + offset[1]) * 1.02,
            font=inputs_font,
            color=BLACK,
        )
        self.draw_text(
            f"{(current_piece.current_house.custom_price) * 0.05:.2f}",
            (aluguel_interact.x * zoom + offset[0]) * 1.08,
            (aluguel_interact.y * zoom + offset[1]) * 1.02,
            font=inputs_font,
            color=BLACK,
        )

    # Método auxiliar para carregar imagens
    def load_image(
        self, filename: str, size: Optional[Tuple[int, int]] = None
    ) -> Optional[pygame.Surface]:
        """
        Carrega uma imagem do diretório src/assets/tiles e redimensiona, se necessário.

        :param filename: Nome do arquivo da imagem.
        :param size: Tupla (largura, altura) para redimensionar a imagem. Se None, mantém o tamanho original.
        :return: Objeto Surface da imagem carregada ou None em caso de erro.
        """
        path: str = f"src/assets/tiles/{filename}"  # Caminho completo para o arquivo
        try:
            image: pygame.Surface = pygame.image.load(
                path
            ).convert_alpha()  # Carregar imagem com transparência
            if size:  # Redimensionar a imagem, se necessário
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {path}: {e}")
            return None

    # Método para criar o mapeamento de nomes para imagens
    def get_image_map(
        self, size: Tuple[int, int]
    ) -> Dict[str, Optional[pygame.Surface]]:
        """
        Cria um dicionário que mapeia nomes personalizados para imagens redimensionadas.

        :param size: Tupla (largura, altura) para redimensionar as imagens.
        :return: Dicionário mapeando nomes para imagens.
        """
        custom_names: List[str] = CUSTOM_NAMES
        image_filenames: List[str] = IMAGE_FILENAMES

        image_map: Dict[str, Optional[pygame.Surface]] = {
            custom_name: self.load_image(filename, size=size)
            for custom_name, filename in zip(custom_names, image_filenames)
        }
        return image_map

    def is_user_registered(self, username: str) -> bool:
        """Verifica se o usuário já está registrado no arquivo."""
        try:
            with open(self.users_file, "r") as file:
                users: List[str] = file.readlines()
            return username in (user.strip() for user in users)
        except FileNotFoundError:
            return False

    def register_user(self, username: str) -> None:
        """Registra um novo usuário no arquivo."""
        with open(self.users_file, "a") as file:
            file.write(f"{username}\n")
