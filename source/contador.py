import pygame as pg


class Contador:
    def __init__(self, janela, c):

        self.cor = (0, 0, 0)
        self.janela = janela
        self.tempo = c

        self.fonte = pg.font.Font(None, 49)
        self.texto = self.fonte.render("Tempo:" + str(c), True, self.cor)

        self.start = True

    def contar(self):
        self.c -= 1

        self.janela.fill((255, 255, 255))
        self.janela.blit(self.texto, [0, 0])
        minutos = self.tempo//60000
        segundos = self.tempo//1000
        self.texto = self.fonte.render(
            "Tempo:" + f'{minutos}:{segundos}', True, self.cor)
