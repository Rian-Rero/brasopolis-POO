import pygame
from house import AbstractHouse
class Interact(AbstractHouse):
    """Representa uma Interação no tabuleiro."""

    def __init__(self, name, custom_name, custom_type, x, y, width, height):
        super().__init__(name, custom_name, custom_type, x, y, width, height)

    def is_available(self):
        """Implementação padrão para interações."""
        return True