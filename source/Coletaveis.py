import pygame as pg
import pygame
from Cores import coresRGB


class Coletaveis(pg.sprite.Sprite):
    def __init__(self, x: float, y: float, janela: pg.Surface, som, altura: float = 40, largura: float = 40):
        super().__init__
        self.x = x
        self.y = y
        self.janela = janela
        self.altura = altura
        
        self.som = som
        self.image = pg.transform.scale(self.image, (largura, altura))

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def deletar(self, lista: list):
        lista.remove(self)

    def desenhar(self):
        self.janela.blit(self.image, self.rect)


class Chave(Coletaveis):
    coletou_chave = False
    chave_ativa = []

    def __init__(self, x: float, y: float, janela: pg.Surface, som, altura: float = 40, largura: float = 40):
        
        Chave.chave_ativa.append(self)
        self.image = pg.image.load("assets/Coletaveis/chave.png")
        self.sprites = []
        for i in range(4):
            img = self.image.subsurface((i*64, 0), (64, 64))
            img = pg.transform.scale(img, (largura, altura))
            self.sprites.append(img)

        self.atual = 0
        self.image = self.sprites[self.atual]
        super().__init__(x, y, janela, som)

    def coletar(self):
        Chave.coletou_chave = True
        print('Coletou a chave!')
        Chave.chave_ativa.clear()

    def update(self, personagem):
        for chave in Chave.chave_ativa:
            chave.atual += 0.3
            if chave.atual >= len(self.sprites):
                chave.atual = 0
            chave.image = self.sprites[int(chave.atual)]
            chave.desenhar()

            # Verificando colisao com o personagem
            if personagem.rect.colliderect(self.rect):
                self.coletar()
                self.som.play()


class Relogio(Coletaveis):
    tempo_restante = 50
    tempos_ativos = []
    dt = 0

    def __init__(self, x: float, y: float, janela: pg.Surface, som, contador, altura: float = 40, largura: float = 40, tempo_extra: float = 5):
        
        Relogio.tempos_ativos.append(self)

        self.contador = contador
        self.tempo_extra = tempo_extra
        self.image = pg.image.load("assets/Coletaveis/relogio_spritesheet.png")

        self.sprites = []
        for i in range(6):
            img = self.image.subsurface((i*160, 0), (160, 160))
            img = pg.transform.scale(img, (largura, altura))
            self.sprites.append(img)

        self.atual = 0
        self.image = self.sprites[self.atual]
        super().__init__(x, y, janela, som)

    def coletar(self):
        Relogio.tempo_restante += self.tempo_extra
        print('Aumentou o tempo restante em', self.tempo_extra, 'segundos')
        self.contador.bonus = True
        self.contador.tempo += self.tempo_extra
        self.deletar(Relogio.tempos_ativos)

    def update(self, personagem, altura: float = 40, largura: float = 40):

        for relogio in Relogio.tempos_ativos:
            relogio.atual += 0.3
            if relogio.atual >= len(self.sprites):
                relogio.atual = 0
            relogio.image = self.sprites[int(relogio.atual)]
            relogio.desenhar()

            # Verificando colisao com o personagem
            if personagem.rect.colliderect(relogio.rect):
                relogio.coletar()
                self.som.play()


class Moeda(Coletaveis):
    moedas_coletadas = 0
    moedas_ativas = []


    def __init__(self, x: float, y: float, janela: pg.Surface, som, altura: float = 40, largura: float = 40):
        
        Moeda.moedas_ativas.append(self)

        self.image = pg.image.load("assets/Coletaveis/moeda.png")
        self.sprites = []
        for i in range(4):
            img = self.image.subsurface((i*64, 0), (64, 64))
            img = pg.transform.scale(img, (largura, altura))
            self.sprites.append(img)

        self.atual = 0
        self.image = self.sprites[self.atual]
        super().__init__(x, y, janela, som)

    def coletar(self):
        Moeda.moedas_coletadas += 1
        print(f'Total de moedas coletadas: {Moeda.moedas_coletadas}')
        self.deletar(Moeda.moedas_ativas)

    def update(self, personagem):
        for moeda in Moeda.moedas_ativas:
            moeda.atual += 0.3
            if moeda.atual >= len(self.sprites):
                moeda.atual = 0
            moeda.image = self.sprites[int(moeda.atual)]
            moeda.desenhar()

            # Verificando colisao com o personagem
            if personagem.rect.colliderect(moeda.rect):
                moeda.coletar()
                self.som.play()

class contadorColetaveis():
    def __init__(self, janela):
        self.janela = janela
        self.fonte = pg.font.Font(None, 45)
    
    def mostrarContador(self):
        
        # Mostrando as moedas
        text_moedas = self.fonte.render(f'Moedas: {Moeda.moedas_coletadas}' , True, coresRGB['branco'])
        text_moedasRect = text_moedas.get_rect()
        text_moedasRect.topright = (770, 5)
        self.janela.blit(text_moedas, text_moedasRect)

        # Mostrando a chave
        text_chave = self.fonte.render(f'Chave: {Chave.coletou_chave}' , True, coresRGB['branco'])
        text_chaveRect = text_chave.get_rect()
        text_chaveRect.topright = (570, 5)
        self.janela.blit(text_chave, text_chaveRect)