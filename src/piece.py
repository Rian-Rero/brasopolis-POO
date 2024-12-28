import pygame


class Piece:
    def __init__(self, color, initial_house):
        self.color = color
        self.current_house = initial_house
        self.position = initial_house.rect.center

    def move_to(self, house):
        """Move a peça para uma nova casa."""
        self.current_house = house
        self.position = house.rect.center

    def draw(self, screen, zoom, offset):
        """Desenha a peça considerando o zoom e deslocamento do tabuleiro."""
        # Ajustar posição ao zoom
        scaled_position = (
            int(self.position[0] * zoom + offset[0]),
            int(self.position[1] * zoom + offset[1]),
        )
        pygame.draw.circle(screen, self.color, scaled_position, int(40 * zoom))
