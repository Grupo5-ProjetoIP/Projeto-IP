import pygame as pg
from Cores import coresRGB


class Contador:
    def __init__(self, janela, tempo, tempo_bonus):

        relogio_imagem = pg.image.load(
            "assets/Coletaveis/relogio_spritesheet.png")
        relogio_imagem = relogio_imagem.subsurface((160*2, 0), (160, 160))
        self.relogio_imagem = pg.transform.scale(relogio_imagem, (64, 64))
        self.relogiorect = relogio_imagem.get_rect()
        self.relogiorect.topleft = (35, 623)

        self.cor = coresRGB["branco"]
        self.janela = janela

        self.bonus = False
        self.tempo_bonus = tempo_bonus

        self.tempo = tempo
        self.ultima_contagem = pg.time.get_ticks()
        minutos = self.tempo//60
        segundos = self.tempo - minutos * 60

        if segundos < 10:
            segundos = f"0{segundos}"

        self.fonte = pg.font.Font(None, 49)
        self.texto = self.fonte.render(
            f'{minutos}:{segundos}', True, self.cor)

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
                    f'{minutos}:{segundos}  +{self.tempo_bonus}s', True, self.cor)
                self.bonus = False
            else:
                self.texto = self.fonte.render(
                    f'{minutos}:{segundos}', True, self.cor)

    def desenhar_contador(self):
        self.janela.blit(self.texto, (100, 635))
        self.janela.blit(self.relogio_imagem, self.relogiorect)

    def update(self):
        self.contar()
