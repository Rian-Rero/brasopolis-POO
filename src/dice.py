import pygame
import random
from constants import *


class Dice:
    def __init__(self, position, size=(100, 50)):
        """
        Inicializa o dado com uma posição e tamanho para o botão.
        :param position: Tupla (x, y) indicando a posição do botão na tela.
        :param size: Tupla (largura, altura) indicando o tamanho do botão.
        """
        self.position = position
        self.size = size
        self.result = None
        self.button_rect = pygame.Rect(position[0], position[1], size[0], size[1])

    def roll(self):
        """
        Gira o dado e retorna um valor entre 1 e 6.
        """
        self.result = random.randint(1, 6)
        return self.result

    def draw(self, screen):
        """
        Desenha o botão do dado na tela.
        :param screen: Superfície do Pygame onde o botão será desenhado.
        """
        # Desenhar o botão
        pygame.draw.rect(screen, (200, 200, 200), self.button_rect)  # Retângulo cinza
        pygame.draw.rect(screen, (BLACK), self.button_rect, 2)  # Borda preta

        # Desenhar o texto "Girar"
        font = pygame.font.Font(None, 36)
        text = font.render("Girar", True, (BLACK))
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)

        # Mostrar o resultado do dado, se existir
        if self.result is not None:
            result_text = font.render(f"Dado: {self.result}", True, (BLACK))
            result_text_rect = result_text.get_rect(
                center=(self.position[0] + 50, self.position[1] - 30)
            )
            screen.blit(result_text, result_text_rect)

    def handle_event(self, event):
        """
        Verifica se o botão foi clicado.
        :param event: Evento do Pygame.
        :return: O valor do dado girado se o botão for clicado, senão None.
        """
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Clique com o botão esquerdo do mouse
            if self.button_rect.collidepoint(event.pos):
                return self.roll()
        return None
