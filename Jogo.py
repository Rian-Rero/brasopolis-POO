from Brasópolis import Dado

class jogo:
    def __init__(self, jogadores, tabuleiro):
        self.jogadores = jogadores 
        self.tabuleiro = tabuleiro
        self.dado = Dado()
        self.jogador_atual = 0
        self.jogo_em_andamento = True

    def iniciar (self):
        print ("Bem vindo ao Brasópolis")
        self.jogador_atual = self.jogadores[0] #determina o primeiro jogador como o jogador 0 da lista7


    def turno(self):
        print(f"vez do {self.jogador_atual.nome}")

        jogar_dado = self.dado.jogar()
        print (f"{self.jogador_atual.nome} tirou {jogar_dado} nos dados")

        self.jogador_atual.mover(jogar_dado, self.tabuleiro)

        casa_atual = self.tabuleiro.casas[self.jogador_atual.posicao]
        print(f"O jogador {self.jogador_atual.nome} parou na casa {casa_atual}")

        casa_atual.acao(self.jogador_atual)

        if self.jogador_atual.saldo <= 0:
            print(f"O jogador {self.jogador_atual.nome} foi à falência!")
            self.jogadores.remove(self.jogador_atual)

    #PRECISA AINDA FAZER A FUNÇÃO DE DETERMINAR O PRÓXIMO JOGADOR, PODE SER POR UM NÚMERO DETERMINADO ANTERIORMENTE PARA CADA JOGADOR
        

