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
        player.gain_money(self.amount)
        print(f"{player.name} ganhou {self.amount}! Novo saldo: {player.balance}")

class LoseMoney(Cart):
    def __init__(self, description, amount):
        super().__init__(description)
        self.amount = 300000

    def executeAction(self, player):
        player.lose_money(self.amount)
        print(f"{player.name} perdeu {self.amount}! Novo saldo: {player.balance}")