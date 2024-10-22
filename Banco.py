class Banco:
    def __init__(self):
        self.saldo_atual = 20000
        self.propriedades_hipotecadas

    def jogador_saldo(self):
        self.propriedades_hipotecadas = []  #define as propriedades que o usuário possui

    def receber_pagamento(self, jogador, valor):
        jogador.pagar(valor)
        self.saldo_total += valor
        print(f"o banco recebeu {valor} do jogador {jogador.nome}. Saldo do banco: {self.saldo_total}")

    def pagar_jogador(self, jogador, valor):
        if self.saldo_total >= valor:
            jogador.receber(valor)
            self.saldo_total -= valor
            print(f"O banco pagou {valor} para o jogador {jogador.nome}")
        else:
            print("O banco não tem dinheiro suficiente para pagar o jogador")

    def hipotecar_propriedade(self,jogador,propriedade, valor_hipoteca):
        jogador.pagar(valor_hipoteca)
        self.propriedades_hipotecadas.append(propriedade)
        print(f"A propriedade {propriedade.nome} foi hipotecada pelo jogador {jogador.nome} pelo valor de {valor_hipoteca}")

    def resgatar_hipoteca(self, jogador, propriedade, valor_resgate):
        if propriedade in self.propriedades_hipotecadas:
            jogador.receber(valor_resgate)
            self.propriedades_hipotecadas.remove(propriedade)
            print(f"A propriedade {propriedade.nome} foi resgatada pelo jogador {jogador.nome} pelo valor de {valor_resgate}")
        else:
            print(f"A propriedade {propriedade.nome} não está hipotecada")

    