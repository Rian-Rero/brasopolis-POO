import pygame
from abc import ABC, abstractmethod
from house import AbstractHouse

class AbstractInteract(AbstractHouse, ABC):
    """Classe abstrata para representar uma interação no tabuleiro."""

    def __init__(self, name: str, custom_name: str, custom_type: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__(name, custom_name, custom_type, x, y, width, height)

    @abstractmethod
    def is_available(self) -> bool:
        pass

class TextInteract(AbstractInteract):
    """Representa uma interação de texto no tabuleiro."""

    def __init__(self, name: str, custom_name: str, custom_type: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__(name, custom_name, custom_type, x, y, width, height)

    def is_available(self) -> bool:
        """Implementação específica para interações de texto."""
        return True

class ButtonInteract(AbstractInteract):
    """Representa uma interação de botão no tabuleiro."""

    def __init__(self, name: str, custom_name: str, custom_type: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__(name, custom_name, custom_type, x, y, width, height)
        self._enabled: bool = True

    def is_available(self) -> bool:
        """Implementação específica para interações de botão."""
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        """Define se o botão está habilitado ou não."""
        self._enabled = enabled