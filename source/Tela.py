import pygame as pg


class Tela:
    def __init__(self, largura: int, altura: int, cor_fundo: tuple):
        self.largura = largura
        self.altura = altura
        self.cor_fundo = cor_fundo

    def criar_tela(self) -> pg.Surface:
        """Cria uma janela"""

        # cria a tela
        tela = pg.display.set_mode((self.largura, self.altura))

        # define a cor de fundo
        tela.fill(self.cor_fundo)

        # define o título
        titulo = "Cin Maze"
        pg.display.set_caption(titulo)

        return tela
