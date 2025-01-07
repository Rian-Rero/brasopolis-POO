class Player:
    def __init__(self, name, money=2000000):
        self.name = name
        self.position = 0
        self.money = money

    def move(self, steps):
        self.position = (self.position + steps) % 40

    def can_afford(self, amount):
        return self.money >= amount
    
    def subtract_money(self,amount):
        if self.can_afford(amount):
            self.money -= amount
            return True
        else:
            return False