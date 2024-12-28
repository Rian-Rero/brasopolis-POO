from Cards import GainMoney, LoseMoney

class Player:
    def __init__(self, name, balance, position, properties=None, isRested=True):
        self.name = name
        self.balance = balance
        self.position = position
        self.properties = properties
        self.isRested = isRested

    def pay(self, value):
        if self.balance >= value:
            self.balance -= value
            print(
                f"The player {self.name} paid {value}. Current balance: {self.balance}"
            )
        else:
            print(f"The player {self.name} does not have enough money to pay {value}.")

    def receive(self, value):
        self.balance += value
        print(
            f"The player {self.name} received {value}. Current balance: {self.balance}"
        )

    def gain_money(self, amount):
        self.receive(amount)

    def lose_money(self, amount):
        self.pay(amount)

