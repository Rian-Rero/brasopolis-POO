from typing import Optional
import pygame
from abc import ABC, abstractmethod
from typing import Optional
from player import FirstPlayer


class AbstractHouse(ABC):
    """Classe abstrata para representar elementos no tabuleiro."""

    def __init__(
        self,
        name: str,
        custom_name: str,
        custom_type: str,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        self.name: str = name
        self.custom_name: str = custom_name
        self.custom_type: str = custom_type
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)

    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o elemento está Disponível para interação."""
        pass


class House(AbstractHouse):
    """Representa uma casa no tabuleiro."""

    def __init__(
        self,
        name: str,
        custom_name: str,
        custom_type: str,
        custom_price: int,
        custom_gain: int,
        custom_loss: int,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        super().__init__(name, custom_name, custom_type, x, y, width, height)
        self.custom_price: int = custom_price
        self.custom_gain: int = custom_gain
        self.custom_loss: int = custom_loss
        self.owner: Optional[FirstPlayer] = None
        self.status: str = "Disponível"
        self.rent_turns_left: int = 0

    def __repr__(self) -> str:
        return f"House(name={self.name})"

    def is_owned(self) -> bool:
        return self.owner is not None

    def reset_rent(self) -> None:
        self.owner = None
        self.status = "Disponível"
        self.rent_turns_left = 0

    def rent(self, turns: int) -> None:
        """Configura o número de turnos que a casa ficará alugada."""
        self.rent_turns_left = turns

    def update_rent(self) -> None:
        """Reduz os turnos de aluguel a cada rodada."""
        if self.rent_turns_left > 0:
            self.rent_turns_left -= 1

    def is_available(self) -> bool:
        """Verifica se a casa está Disponível para compra ou aluguel."""
        return self.rent_turns_left == 0 and self.owner is None

    def getOwner(self) -> str:
        if self.owner:
            return self.owner.name
        return "Nenhum"
