from abc import ABC, abstractmethod
from typing import Optional

class AbstractPlayer(ABC):
    """Classe abstrata para representar um jogador."""

    def __init__(self, name: str, money: int = 2000000) -> None:
        self._name: str = name
        self._position: int = 0
        self._money: int = money

    @abstractmethod
    def move(self, steps: int) -> None:
        pass

    @abstractmethod
    def can_afford(self, amount: int) -> bool:
        pass

    @abstractmethod
    def subtract_money(self, amount: int) -> bool:
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> int:
        return self._position

    @property
    def money(self) -> int:
        return self._money

    @money.setter
    def money(self, amount: int) -> None:
        self._money = amount

class FirstPlayer(AbstractPlayer):
    """Classe para representar o primeiro tipo de jogador."""

    def __init__(self, name: str, money: int = 2000000) -> None:
        super().__init__(name, money)

    def move(self, steps: int) -> None:
        """Move o jogador um número específico de passos."""
        self._position = (self._position + steps) % 40

    def can_afford(self, amount: int) -> bool:
        """Verifica se o jogador pode pagar uma quantia específica."""
        return self._money >= amount

    def subtract_money(self, amount: int) -> bool:
        """Subtrai uma quantia de dinheiro do jogador."""
        if self.can_afford(amount):
            self._money -= amount
            return True
        else:
            return False

class SecondPlayer(AbstractPlayer):
    """Classe para representar o segundo tipo de jogador."""

    def __init__(self, name: str, money: int = 2000000) -> None:
        super().__init__(name, money)

    def move(self, steps: int) -> None:
        """Move o jogador um número específico de passos."""
        self._position = (self._position + steps) % 40

    def can_afford(self, amount: int) -> bool:
        """Verifica se o jogador pode pagar uma quantia específica."""
        return self._money >= amount

    def subtract_money(self, amount: int) -> bool:
        """Subtrai uma quantia de dinheiro do jogador."""
        if self.can_afford(amount):
            self._money -= amount
            return True
        else:
            return False