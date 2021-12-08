import pygame as pg


class Personagem:
    """Um personagem simples que anda pela tela"""

    # inicializa os atributos
    def __init__(self, janela: pg.Surface,
                 x: float, y: float, largura: float, altura: float, velocidade: float, cor: tuple):

        self.janela = janela
        self.x = x
        self.y = y

        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.cor = cor

    def desenhar(self):
        """desenha o personagem na tela"""

        retangulo = pg.Rect(self.x, self.y, self.largura, self.altura)
        pg.draw.rect(self.janela, self.cor, retangulo)

    def mover(self):
        """move o personagem de acordo com a tecla pressionada"""

        # armazena a tecla pressionada
        keys = pg.key.get_pressed()

        # move para a esquerda
        if keys[pg.K_a] and self.x - self.velocidade >= 0:
            self.x -= self.velocidade

        # move para a direita
        if keys[pg.K_d] and self.x + self.largura + self.velocidade <= self.janela.get_width():
            self.x += self.velocidade

        # move para cima
        if keys[pg.K_w] and self.y - self.velocidade >= 0:
            self.y -= self.velocidade

        # move para baixo
        if keys[pg.K_s] and self.y + self.altura + self.velocidade <= self.janela.get_height():
            self.y += self.velocidade
