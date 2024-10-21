class Tabuleiro:
    def __init__(self, nome):
        self.nome = nome #NOME NÃO ESTÁ DEFINIDO, COLOQUEI SÓ PARA NÃO DAR PAU NO VS


class Casa:
    def __init__(self, nome):
        self.nome = nome

        def acao(self, jogador):
            print(f"O jogador {jogador.nome} parou em {self.nome}")