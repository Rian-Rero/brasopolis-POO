from Player import Player
class Properties:
    def __init__(self, name, price, rent, owner):
        self.name = name
        self.price = price
        self.remt = rent
        self.ownerID = None
    def buy(self, player):
        if self.owner is None:  
            if player.money >= self.price: 
                player.money -= self.price  
                self.owner = player          
                print(f"{player.name} comprou {self.name} por {self.price}.")
            else:
                print(f"{player.name} não tem dinheiro suficiente para comprar {self.name}.")
        else:
            print(f"{self.name} já pertence a {self.owner.name}.")

    def PayRent(self, player):
        if self.owner is not None and self.owner != player:
            player.money -= self.rent
            self.owner.money += self.rent 
            print(f"{player.name} pagou {self.rent} de aluguel para {self.owner.name} por {self.name}.")
        elif self.owner is None:
            print(f"{self.name} está disponível para compra.")
        else:
            print(f"{player.name} não precisa pagar aluguel por {self.name} pois é o proprietário.")
