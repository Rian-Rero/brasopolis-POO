class Bank:
    def __init__(self):
        self.currentBalance = 200000000
        self.mortgagedProperties = []

    def playerProperties(self):
        return self.mortgagedProperties

    def receivePayment(self, player, value):
        player.pay(value)
        self.currentBalance += value
        print(
            f"o bank received {value} from player {player.name}. Bank balance: {self.currentBalance}"
        )

    def payPlayer(self, player, value):
        if self.currentBalance >= value:
            player.receive(value)
            self.currentBalance -= value
            print(f"The bank paid {value} to player {player.name}")
        else:
            print("The bank does not have enough money to pay the player")

    def mortgageProperty(self, player, property, mortgageValue):
        player.pay(mortgageValue)
        self.mortgagedProperties.append(property)
        print(
            f"The property {property.name} was mortgaged by player {player.name} for the value of {mortgageValue}"
        )

    def redeemMortgage(self, player, property, redemptionValue):
        if property in self.mortgagedProperties:
            player.receive(redemptionValue)
            self.mortgagedProperties.remove(property)
            print(
                f"The property {property.name} was redeemed by player {player.name} for the value of {redemptionValue}"
            )
        else:
            print(f"The property {property.name} is not mortgaged")
