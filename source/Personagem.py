import pygame as pg
from Cores import coresRGB


class Personagem(pg.sprite.Sprite):
    """Um personagem simples que anda pela tela"""

    # inicializa os atributos
    def __init__(self, janela: pg.Surface,
                 x: float, y: float, largura: float, altura: float, velocidade: float, cor: tuple, imagem: pg.Surface):

        super().__init__()

        self.janela = janela

        self.largura = largura
        self.altura = altura

        self.cor = cor

        self.imagem = pg.transform.scale(imagem, (self.largura, self.altura))

        self.retangulo = self.imagem.get_rect()
        self.retangulo.x = x
        self.retangulo.y = y

        self.velocidade = velocidade

    def desenhar(self):
        """desenha o personagem na tela"""

        self.janela.blit(self.imagem, self.retangulo)

    def mover(self):
        """move o personagem de acordo com a tecla pressionada"""

        # armazena a tecla pressionada
        keys = pg.key.get_pressed()

        # move para a esquerda
        if keys[pg.K_a] and self.retangulo.x - self.velocidade >= 0:
            self.retangulo.x -= self.velocidade

        # move para a direita
        if keys[pg.K_d] and self.retangulo.x + self.largura + self.velocidade <= self.janela.get_width():
            self.retangulo.x += self.velocidade

        # move para cima
        if keys[pg.K_w] and self.retangulo.y - self.velocidade >= 0:
            self.retangulo.y -= self.velocidade

        # move para baixo
        if keys[pg.K_s] and self.retangulo.y + self.altura + self.velocidade <= self.janela.get_height():
            self.retangulo.y += self.velocidade

    def update(self):
        """função executada a cada ciclo"""

        self.mover()
        self.janela.fill(coresRGB["branco"])
        self.desenhar()
