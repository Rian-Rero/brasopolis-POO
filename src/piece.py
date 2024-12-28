import pygame


class Piece:
    """Representa uma peça que se move no tabuleiro."""

    def __init__(self, color, initial_house):
        self.color = color
        self.current_house = initial_house
        self.position = initial_house.rect.center

    def move_to(self, house):
        """Move a peça para uma nova casa."""
        self.current_house = house
        self.position = house.rect.center

    def draw(self, screen):
        """Desenha a peça na posição atual."""
        pygame.draw.circle(screen, self.color, self.position, 15)
