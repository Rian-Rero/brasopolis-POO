import random

class Dice:
    def roll(self):
        return random.randint(1, 6)
        

def main():
    dado=Dice()
    resultado=dado.roll()
    print("Resultado do lançamento dos dados:", resultado)
main()