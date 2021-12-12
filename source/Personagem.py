import pygame as pg
from pygame import sprite
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

        self.velocidade = velocidade
        self.andando = False

        self.cor = cor

        # cria uma lista com os sprites da animação
        self.sprite_sheet = imagem
        self.sprites = []
        self.atual = 0

        qtd_sprt = 12
        altura_sprt = self.sprite_sheet.get_height()

        for i in range(qtd_sprt):
            image = self.sprite_sheet.subsurface(
                (i*altura_sprt, 0), (altura_sprt, altura_sprt))
            image = pg.transform.scale(
                image, (self.largura * 2, self.altura * 2))
            self.sprites.append(image)

        # define as imagens para cada direção
        self.sprites_cima = list(self.sprites)

        self.sprites_baixo = []
        for i in self.sprites:
            i = pg.transform.flip(i, False, True)
            self.sprites_baixo.append(i)

        self.sprites_direita = []
        for i in self.sprites:
            i = pg.transform.rotate(i, -90)
            self.sprites_direita.append(i)

        self.sprites_esquerda = []
        for i in self.sprites_direita:
            i = pg.transform.flip(i, True, False)
            self.sprites_esquerda.append(i)

        # define a imagem inicial e o retângulo
        self.image = self.sprites[0]
        self.rect = pg.Rect(x, y, self.largura, self.altura)

    def desenhar(self):
        """desenha o personagem na tela"""

        offset = (self.rect.x - self.image.get_height() * 0.23,
                  self.rect.y - self.image.get_height() * 0.23)

        if self.andando:
            self.janela.blit(self.image, offset)
        else:
            self.janela.blit(self.sprites[0], offset)

    def andar(self):
        """animação do personagem"""

        keys = pg.key.get_pressed()
        self.andando = True

        if keys[pg.K_a]:
            self.sprites = self.sprites_esquerda
            if keys[pg.K_d]:
                self.andando = False
        elif keys[pg.K_d]:
            self.sprites = self.sprites_direita
        elif keys[pg.K_w]:
            self.sprites = self.sprites_cima
            if keys[pg.K_s]:
                self.andando = False
        elif keys[pg.K_s]:
            self.sprites = self.sprites_baixo
        else:
            self.andando = False

        if self.andando:
            self.atual += 0.6
            if self.atual >= len(self.sprites):
                self.atual = 0
            self.image = self.sprites[int(self.atual)]

    def colisao_com_labirinto(self, direcao: str) -> bool:
        """checa se é possível andar sem colidir com o labirinto"""

        sprite_aux = pg.sprite.Sprite()
        sprite_aux.image = pg.Surface(self.rect.size)
        sprite_aux.image.fill(coresRGB["preto"])

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
        self.andar()
        self.janela.fill(coresRGB["branco"])
        self.janela.blit(self.labirinto.image, self.labirinto.rect)
        self.desenhar()
