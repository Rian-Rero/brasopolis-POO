import random

class Dice:
    def roll(self):
        return random.randint(1, 6)
        

def main():
    dado=Dice()
    resultado=dado.roll()
    print(resultado)
main()