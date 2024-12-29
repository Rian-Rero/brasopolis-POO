import pygame
from constants import *


class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 35)
        self.users_file = "src/DataBase/users.txt"

    def show_player_count_selection(self):
        """Exibe uma tela para o jogador selecionar a quantidade de jogadores."""
        running = True
        selected_count = None
        while running:
            self.screen.fill((45, 86, 80))
            self.draw_text(
                "Selecione o número de jogadores (2 a 4):",
                self.screen.get_width() // 2,
                100,
            )

            # Botões para 2, 3 ou 4 jogadores
            screen_width, screen_height = self.screen.get_size()
            button_width, button_height = screen_width // 6, screen_height // 12

            buttons = {
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

    def show_login_screen(self, player_count):
        """Exibe a tela de login/cadastro para o número de jogadores."""
        players = []
        for i in range(1, player_count + 1):
            running = True
            username = ""
            while running:
                self.screen.fill((45, 86, 80))
                self.draw_text(
                    f"Jogador {i}: Digite seu nome:", self.screen.get_width() // 2, 100
                )

                # Campo de texto
                input_box = pygame.Rect(300, 200, 400, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), input_box)
                self.draw_text(
                    username, input_box.x + 10, input_box.y + 10, font=self.small_font
                )

                # Botão de confirmar
                confirm_button = pygame.Rect(350, 300, 200, 50)
                pygame.draw.rect(self.screen, (111, 185, 174), confirm_button)
                self.draw_text(
                    "Confirmar",
                    confirm_button.centerx,
                    confirm_button.centery,
                    font=self.small_font,
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

    def draw_text(self, text, x, y, font=None, color=(BLACK)):
        """Desenha texto na tela."""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_text_simple(self, text, x, y, font=None, color=(BLACK)):
        """Desenha texto na tela nas coordenadas fornecidas."""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        # A posição será diretamente nas coordenadas (x, y)
        self.screen.blit(text_surface, (x, y))

    def draw_interface(
        self, screen, current_player, current_piece, interact, zoom, offset
    ):
        """Exibe informações sobre o jogador atual e outras estatísticas do jogo."""
        # Atualizar a lógica para o jogador atual corretamente
        screen_width = screen.get_width()
        player_interact = next((i for i in interact if i.custom_name == "Player"), None)
        saldo_interact = next((i for i in interact if i.custom_name == "Saldo"), None)
        cidade_interact = next((i for i in interact if i.custom_name == "Cidade"), None)
        proprietario_interact = next(
            (i for i in interact if i.custom_name == "Proprietario"), None
        )
        aluguel_interact = next(
            (i for i in interact if i.custom_name == "Aluguel"), None
        )
        # Nome do jogador atual
        self.draw_text(
            f"{current_player.name}",
            (player_interact.x * zoom + offset[0]) * 1.45,
            (player_interact.y * zoom + offset[1]) * 1.05,
            font=self.small_font,
            color=(BLACK),
        )

        # Mostrar saldo do jogador atual
        self.draw_text(
            f"{current_player.money:.2f}",
            (saldo_interact.x * zoom + offset[0]) * 1.25,
            (saldo_interact.y * zoom + offset[1]) * 1.03,
            font=self.small_font,
            color=(BLACK),
        )

        # Imagem do jogador atual
        image_map = self.get_image_map()
        image = image_map.get(current_piece.current_house.custom_name)
        if image:
            screen.blit(image, (1780, 350))

        self.draw_text(
            f"{current_piece.current_house.custom_name}",
            (cidade_interact.x * zoom + offset[0]) * 1.1,
            (cidade_interact.y * zoom + offset[1]) * 1.02,
            font=self.small_font,
            color=(BLACK),
        )

        self.draw_text(
            f"{current_piece.current_house.custom_price:.2f}",
            (aluguel_interact.x * zoom + offset[0]) * 1.08,
            (aluguel_interact.y * zoom + offset[1]) * 1.02,
            font=self.small_font,
            color=(BLACK),
        )

    # Método auxiliar para carregar imagens
    def load_image(self, filename, size=None):
        """
        Carrega uma imagem do diretório src/assets/tiles e redimensiona, se necessário.

        :param filename: Nome do arquivo da imagem.
        :param size: Tupla (largura, altura) para redimensionar a imagem. Se None, mantém o tamanho original.
        :return: Objeto Surface da imagem carregada ou None em caso de erro.
        """
        path = f"src/assets/tiles/{filename}"  # Caminho completo para o arquivo
        try:
            image = pygame.image.load(
                path
            ).convert_alpha()  # Carregar imagem com transparência
            if size:  # Redimensionar a imagem, se necessário
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {path}: {e}")
            return None

    # Método para criar o mapeamento de nomes para imagens
    def get_image_map(self, size=(500, 550)):
        """
        Cria um dicionário que mapeia nomes personalizados para imagens redimensionadas.

        :param size: Tupla (largura, altura) para redimensionar as imagens.
        :return: Dicionário mapeando nomes para imagens.
        """
        custom_names = CUSTOM_NAMES
        image_filenames = IMAGE_FILENAMES

        image_map = {
            custom_name: self.load_image(filename, size=size)
            for custom_name, filename in zip(custom_names, image_filenames)
        }
        return image_map

    def is_user_registered(self, username):
        """Verifica se o usuário já está registrado no arquivo."""
        try:
            with open(self.users_file, "r") as file:
                users = file.readlines()
            return username in (user.strip() for user in users)
        except FileNotFoundError:
            return False

    def register_user(self, username):
        """Registra um novo usuário no arquivo."""
        with open(self.users_file, "a") as file:
            file.write(f"{username}\n")
