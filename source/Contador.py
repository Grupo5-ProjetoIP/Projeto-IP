import pygame as pg
from Cores import coresRGB


class Contador:
    def __init__(self, janela, tempo):

        self.cor = coresRGB["branco"]
        self.janela = janela

        self.bonus = False

        self.tempo = tempo
        self.ultima_contagem = pg.time.get_ticks()
        minutos = self.tempo//60
        segundos = self.tempo - minutos * 60

        if segundos < 10:
            segundos = f"0{segundos}"

        self.fonte = pg.font.Font(None, 49)
        self.texto = self.fonte.render(
            "Tempo= " + f'{minutos}:{segundos}', True, self.cor)

        self.start = True

    def contar(self):
        self.desenhar_contador()
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - self.ultima_contagem >= 1000:
            self.tempo -= 1
            self.ultima_contagem = tempo_atual
            minutos = self.tempo//60
            segundos = self.tempo - minutos * 60

            if segundos < 10:
                segundos = f"0{segundos}"

            if self.bonus:
                self.texto = self.fonte.render(
                    "Tempo= " + f'{minutos}:{segundos}  +5s', True, self.cor)
                self.bonus = False
            else:
                self.texto = self.fonte.render(
                    "Tempo= " + f'{minutos}:{segundos}', True, self.cor)

    def desenhar_contador(self):
        self.janela.blit(self.texto, [0, 0])

    def update(self):
        self.contar()
