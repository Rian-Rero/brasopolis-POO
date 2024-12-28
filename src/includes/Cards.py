from abc import ABC, abstractmethod

class Cart(ABC):
    def __init__(self, description):
        self.description = description

    @abstractmethod
    def executeAction(self, player):
        pass

class GainMoney(Cart):
    def __init__(self, description, amount):
        super().__init__(description)
        self.amount = 500000

    def executeAction(self, player):
        print(f"Executando ação da carta: {self.description}")
        player.gain_money(self.amount)

class LoseMoney(Cart):
    def __init__(self, description, amount):
        super().__init__(description)
        self.amount = 300000

    def executeAction(self, player):
        print(f"Executando ação da carta: {self.description}")
        player.lose_money(self.amount)