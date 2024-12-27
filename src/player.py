class Player:
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.position = 0

    def move(self, steps):
        self.position = (self.position + steps) % 40
