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
        custom_loss,
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
        self.custom_loss = custom_loss
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.owner = None
        self.status = "disponível"
        self.rent_turns_left = 0

    def __repr__(self):
        return f"House(name={self.name})"

    def is_owned(self):
        return self.owner is not None

    def reset_rent(self):
        self.owner = None
        self.status = "disponível"
        self.rent_turns_left = 0

    def rent(self, turns):
        """Configura o número de turnos que a casa ficará alugada."""
        self.rent_turns_left = turns

    def update_rent(self):
        """Reduz os turnos de aluguel a cada rodada."""
        if self.rent_turns_left > 0:
            self.rent_turns_left -= 1

    def is_available(self):
        """Verifica se a casa está disponível para compra ou aluguel."""
        return self.rent_turns_left == 0 and self.owner is None
