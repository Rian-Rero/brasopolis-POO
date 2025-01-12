import pygame
import random
from constants import *
from typing import Tuple, Optional, Any

class Dice:
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int] = (110, 55)) -> None:
        """
        Inicializa o dado com uma posição e tamanho para o botão.
        :param position: Tupla (x, y) indicando a posição do botão na tela.
        :param size: Tupla (largura, altura) indicando o tamanho do botão.
        """
        self._position: Tuple[int, int] = position
        self._size: Tuple[int, int] = size
        self._result: Optional[int] = None
        self._button_rect: pygame.Rect = pygame.Rect(position[0], position[1], size[0], size[1])

    def roll(self) -> int:
        """
        Gira o dado e retorna um valor entre 1 e 6.
        """
        self.result = random.randint(1, 6)
        return self.result

    def draw(self, screen: pygame.Surface, interact: Any, zoom: float, offset: Tuple[int, int]) -> None:
        """
        Desenha o botão do dado na tela.
        :param screen: Superfície do Pygame onde o botão será desenhado.
        """
        dice_interact = next((i for i in interact if i.custom_name == "Dado"), None)
        jogar_interact = next((i for i in interact if i.custom_name == "Jogar"), None)
        self._button_rect = pygame.Rect(
            (jogar_interact.x * zoom + offset[0]),
            (jogar_interact.y * zoom + offset[1]),
            jogar_interact.width * zoom,
            jogar_interact.height * zoom,
        )
        pygame.draw.rect(
            screen, BUTTON_GREEN, self._button_rect, border_radius=15
        )  # Retângulo Verde

        # Desenhar o texto "JOGAR"
        font_size = round(55 * zoom)
        font = pygame.font.Font(None, font_size)
        text = font.render("JOGAR", True, (WHITE))
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)

        # Mostrar o resultado do dado, se existir
        if self.result is not None:
            result_text = font.render(f"{self.result}", True, (BLACK))
            result_text_rect = result_text.get_rect(
                topleft=(
                    (dice_interact.x * zoom + offset[0]) * 1.04,
                    (dice_interact.y * zoom + offset[1]) * 1.02,
                )
            )
            screen.blit(result_text, result_text_rect)

    def handle_event(self, event: pygame.event.Event) -> Optional[int]:
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

    @property
    def position(self) -> Tuple[int, int]:
        return self.position

    @property
    def size(self) -> Tuple[int, int]:
        return self.size

    @property
    def result(self) -> Optional[int]:
        return self.result

    @property
    def button_rect(self) -> pygame.Rect:
        return self._button_rect