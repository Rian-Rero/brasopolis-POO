from Player import Player
class Properties:
    def __init__(self, name, price, status, rent,  owner):
        self.name=name
        self.price=price
        self.status=True#vendido ou não
        self.rent=rent
        self.owner=owner

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

    def __str__(self):#converte obj em string pra printar
        owner_name = self.owner.name if self.owner else "Nenhum"
        return f"Propriedade: {self.name}, Preço: {self.price}, Status: {'Vendido' if self.status else 'Disponível'}, Aluguel: {self.rent}, Proprietário: {owner_name}"


#aluguel = 5% do valor da prop.
p1=Properties("São Paulo", 950000, True, 47500, None)
p2=Properties("Varginha", 330000, True, 16500, None)
p3=Properties("Ressaquinha", 310000, True, 15500, None)
p4=Properties("Fortaleza", 800000, True, 40000, None)
p5=Properties("Borrazópolis", 140000, True, 7000, None)
p6=Properties("Taubaté", 350000, True, 17500, None)
p7=Properties("Teresina", 420000, True, 22500, None)
p8=Properties("Cuiabá", 700000, True, 35000, None)
p9=Properties("Boa Vista", 650000, True, 16500, None)
p10=Properties("Zebelê", 160000, True, 8000, None)

p11=Properties("Xique-xique", 180000, True, 9000, None)
p12=Properties("Porto Alegre", 850000, True, 42500, None)
p13=Properties("Aracaju", 500000, True, 25000, None)
p14=Properties("Canutama", 230000, True, 11500, None)
p15=Properties("Brasília", 1000000, True, 50000, None)
p16=Properties("Macapá", 600000, True, 30000, None)

p17=Properties("Guiratinga", 150000, True, 7500, None)
p18=Properties("Campo Grande", 650000, True, 32500, None)
p19=Properties("Bombinhas", 400000, True, 20000, None)
p20=Properties("Goiânia", 480000, True, 24000, None)
p21=Properties("Chupinguaia", 200000, True, 10000, None)
p22=Properties("Uauá", 120000, True, 6000, None)
p23=Properties("Belo Horizonte", 900000, True, 45000, None)
p24=Properties("Tracuateua", 250000, True, 12500, None)
p25=Properties("Goianinha", 380000, True, 19000, None)
p26=Properties("Florianópolis", 750000, True, 37500, None)
p27=Properties("Xexéu", 270000, True, 13500, None)

p28=Properties("Tuntum", 210000, True, 10500, None)
p29=Properties("Manaus", 700000, True, 35000, None)
p30=Properties("Rio de Janeiro", 1000000, True, 50000, None)
p31=Properties("Sooretama", 280000, True, 14000, None)
p32=Properties("Rio Branco", 420000, True, 21000, None)

