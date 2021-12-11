import pygame as pg
from Cores import coresRGB


class Personagem(pg.sprite.Sprite):
    """Um personagem simples que anda pela tela"""

    # inicializa os atributos
    def __init__(self, janela: pg.Surface, labirinto: pg.Surface,
                 x: float, y: float, largura: float, altura: float, velocidade: float, cor: tuple, imagem: pg.Surface):

        super().__init__()

        self.janela = janela
        self.labirinto = labirinto

        self.largura = largura
        self.altura = altura

        self.cor = cor

        self.image = pg.transform.scale(imagem, (self.largura, self.altura))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocidade = velocidade

    def desenhar(self):
        """desenha o personagem na tela"""

        self.janela.blit(self.image, self.rect)

    def colisao_com_labirinto(self, direcao: str) -> bool:
        """checa se é possível andar sem colidir com o labirinto"""

        sprite_aux = pg.sprite.Sprite()
        sprite_aux.image = self.image

        if direcao == "esquerda":
            sprite_aux.rect = pg.Rect(
                self.rect.x - self.velocidade, self.rect.y, self.largura, self.altura)

        elif direcao == "direita":
            sprite_aux.rect = pg.Rect(
                self.rect.x + self.velocidade, self.rect.y, self.largura, self.altura)

        elif direcao == "cima":
            sprite_aux.rect = pg.Rect(
                self.rect.x, self.rect.y - self.velocidade, self.largura, self.altura)

        elif direcao == "baixo":
            sprite_aux.rect = pg.Rect(
                self.rect.x, self.rect.y + self.velocidade, self.largura, self.altura)

        else:
            raise ValueError(f"{direcao} não é uma direção")

        if pg.sprite.collide_mask(sprite_aux, self.labirinto):
            return True
        return False

    def mover(self):
        """move o personagem de acordo com a tecla pressionada"""

        # armazena a tecla pressionada
        keys = pg.key.get_pressed()

        # move para a esquerda
        if keys[pg.K_a] and self.rect.x - self.velocidade >= 0 and not self.colisao_com_labirinto("esquerda"):
            self.rect.x -= self.velocidade

        # move para a direita
        if keys[pg.K_d] and self.rect.x + self.largura + self.velocidade <= self.janela.get_width() \
                and not self.colisao_com_labirinto("direita"):
            self.rect.x += self.velocidade

        # move para cima
        if keys[pg.K_w] and self.rect.y - self.velocidade >= 0 and not self.colisao_com_labirinto("cima"):
            self.rect.y -= self.velocidade

        # move para baixo
        if keys[pg.K_s] and self.rect.y + self.altura + self.velocidade <= self.janela.get_height() \
                and not self.colisao_com_labirinto("baixo"):
            self.rect.y += self.velocidade

    def update(self):
        """função executada a cada ciclo"""

        self.mover()
        self.janela.fill(coresRGB["branco"])
        self.janela.blit(self.labirinto.image, self.labirinto.rect)
        self.janela.blit(self.image, self.rect)
