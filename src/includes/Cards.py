class Cart:
    def __init__(self, description, action):
        self.description = description
        self.action = action

    def executeAction(self, player):
        print(f"Executando ação da carta: {self.description}")
        self.action(player)

#colocar abaixo subclasses (usar herança) de cada tipo de carta especial (definir cartas especiais)