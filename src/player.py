class Player:
    def __init__(self, name, money=2000000):
        self.name = name
        self.position = 0
        self.money = money

    def move(self, steps):
        self.position = (self.position + steps) % 40
