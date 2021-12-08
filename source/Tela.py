import pygame as pg


def criar_tela(largura: int, altura: int, cor: tuple) -> pg.Surface:
    """Cria uma janela"""

    # cria a tela
    tela = pg.display.set_mode((largura, altura))

    # define a cor de fundo
    tela.fill(cor)

    # define o título
    titulo = f"tela x={largura}  y={altura}"
    pg.display.set_caption(titulo)

    return tela
