import pygame
from house import AbstractHouse

class Interact(AbstractHouse):
    """Representa uma Interação no tabuleiro."""

    def __init__(self, name: str, custom_name: str, custom_type: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__(name, custom_name, custom_type, x, y, width, height)

    def is_available(self) -> bool:
        """Implementação padrão para interações."""
        return True