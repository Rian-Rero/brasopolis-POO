import pygame


class Interact:
    """Representa uma Interação no tabuleiro."""

    def __init__(self, name, custom_name, custom_type, x, y, width, height):
        self.name = name
        self.custom_name = custom_name
        self.custom_type = custom_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
