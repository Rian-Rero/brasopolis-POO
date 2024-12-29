import pygame


class House:
    """Representa uma casa no tabuleiro."""

    def __init__(
        self,
        name,
        custom_name,
        custom_type,
        custom_price,
        custom_gain,
        x,
        y,
        width,
        height,
    ):
        self.name = name
        self.custom_name = custom_name
        self.custom_type = custom_type
        self.custom_price = custom_price
        self.custom_gain = custom_gain
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def __repr__(self):
        return f"House(name={self.name}"
