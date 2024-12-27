import pygame
from constants import BLACK


class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 35)
        self.users_file = "/caminho/absoluto/users.txt"

    def show_player_count_selection(self):
        """Exibe uma tela para o jogador selecionar a quantidade de jogadores."""
        running = True
        selected_count = None
        while running:
            self.screen.fill((0, 50, 100))
            self.draw_text(
                "Selecione o número de jogadores (2 a 4):",
                self.screen.get_width() // 2,
                100,
            )

            # Botões para 2, 3 ou 4 jogadores
            buttons = {
                "2": pygame.Rect(300, 200, 200, 50),
                "3": pygame.Rect(300, 300, 200, 50),
                "4": pygame.Rect(300, 400, 200, 50),
            }

            # Desenhar botões
            for label, rect in buttons.items():
                pygame.draw.rect(self.screen, (200, 200, 200), rect)
                # Desenhar texto sobre o botão
                self.draw_text(
                    label,
                    rect.centerx,
                    rect.centery,
                    font=self.small_font,
                    color=(0, 0, 0),
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
                self.screen.fill((0, 50, 100))
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
                pygame.draw.rect(self.screen, (200, 200, 200), confirm_button)
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

    def draw_text(self, text, x, y, font=None, color=(255, 255, 255)):
        """Desenha texto na tela."""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
