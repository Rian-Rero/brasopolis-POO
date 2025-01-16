from abc import ABC, abstractmethod
import pygame
from typing import Tuple

class AbstractPiece(ABC):
    """Classe abstrata para representar uma peça no tabuleiro."""

    def __init__(self, color: Tuple[int, int, int], initial_house: pygame.Rect) -> None:
        self._color: Tuple[int, int, int] = color
        self._current_house: pygame.Rect = initial_house
        self._position: Tuple[int, int] = initial_house.rect.center

    @abstractmethod
    def move_to(self, house: pygame.Rect) -> None:
        """Move a peça para uma nova casa."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, zoom: float, offset: Tuple[int, int]) -> None:
        """Desenha a peça considerando o zoom e deslocamento do tabuleiro."""
        pass

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @property
    def current_house(self) -> pygame.Rect:
        return self._current_house

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

class Piece(AbstractPiece):
    def __init__(self, color: Tuple[int, int, int], initial_house: pygame.Rect) -> None:
        super().__init__(color, initial_house)

    def move_to(self, house: pygame.Rect) -> None:
        """Move a peça para uma nova casa."""
        self._current_house = house
        self._position = house.rect.center

    def draw(self, screen: pygame.Surface, zoom: float, offset: Tuple[int, int]) -> None:
        """Desenha a peça considerando o zoom e deslocamento do tabuleiro."""
        # Ajustar posição ao zoom
        scaled_position = (
            int(self._position[0] * zoom + offset[0]),
            int(self._position[1] * zoom + offset[1]),
        )
        pygame.draw.circle(screen, self._color, scaled_position, int(40 * zoom))