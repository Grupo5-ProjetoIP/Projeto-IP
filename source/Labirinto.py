import pygame as pg
from Cores import coresRGB


class Labirinto:
    def __init__(self, image, mascara, tela) -> None:
        self.piso = pg.sprite.Sprite()
        self.piso.image = pg.transform.scale(image, (800, 600))
        self.piso.rect = self.piso.image.get_rect()
        self.parede = pg.sprite.Sprite()
        self.parede.image = pg.transform.scale(mascara, (800, 600))
        self.parede.rect = self.parede.image.get_rect()
        self.tela = tela

    def desenhar_labirinto(self):
        self.tela.blit(self.piso.image, self.piso.rect)
        self.tela.blit(self.parede.image, self.parede.rect)
