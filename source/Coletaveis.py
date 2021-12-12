import pygame as pg

class Coletaveis(pg.sprite.Sprite):
    def __init__(self, x: float, y: float, janela: pg.Surface, image: pg.Surface, altura: float = 40, largura: float = 40):
        super().__init__
        self.x = x
        self.y = y
        self.janela = janela
        self.altura = altura
        self.image = image
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

    def __init__(self, x: float, y: float, janela: pg.Surface, image: pg.Surface, altura: float = 40, largura: float = 40):
        super().__init__(x, y, janela, image)
        Chave.chave_ativa.append(self)

    def coletar(self):
        Chave.coletou_chave = True
        print('Coletou a chave!')
        Chave.chave_ativa.clear()

    def update(self, personagem):
        for chave in Chave.chave_ativa:
            chave.desenhar()
            if personagem.retangulo.colliderect(self.rect):
                self.coletar()
        
class Relogio(Coletaveis):
    tempo_restante = 50
    tempos_ativos = []
    dt = 0
    sprite_sheet = pg.image.load("assets/Coletaveis/relogio_spritesheet.png")

    def __init__(self, x: float, y: float, janela: pg.Surface, image = sprite_sheet, altura: float = 40, largura: float = 40, tempo_extra: float = 25):
        super().__init__(x, y, janela, image)
        Relogio.tempos_ativos.append(self)
        self.tempo_extra = tempo_extra

        self.sprites = []
        for i in range(6):
            img = Relogio.sprite_sheet.subsurface((i*160,0), (160,160))
            img = pg.transform.scale(img, (largura, altura))
            self.sprites.append(img)

        self.atual = 0
        self.image = self.sprites[self.atual]
        
    def coletar(self):
        Relogio.tempo_restante += self.tempo_extra
        print('Aumentou o tempo restante em', self.tempo_extra, 'segundos')
        self.deletar(Relogio.tempos_ativos)
    
    def update(self, personagem, altura: float = 40, largura: float = 40 ):
        
        for relogio in Relogio.tempos_ativos:
            relogio.atual += 0.3
            if relogio.atual >= len(self.sprites):
                relogio.atual = 0
            relogio.image = self.sprites[int(relogio.atual)]
            relogio.desenhar()
            if personagem.retangulo.colliderect(relogio.rect):
                relogio.coletar()
        

class Moeda(Coletaveis):
    moedas_coletadas = 0
    moedas_ativas = []

    def __init__(self, x: float, y: float, janela: pg.Surface, image: pg.Surface, altura: float = 40, largura: float = 40):
        super().__init__(x, y, janela, image)
        Moeda.moedas_ativas.append(self)

    def coletar(self):
        Moeda.moedas_coletadas += 1
        print(f'Total de moedas coletadas: {Moeda.moedas_coletadas}')
        self.deletar(Moeda.moedas_ativas)
    
    def update(self, personagem):
        for moeda in Moeda.moedas_ativas:
            moeda.desenhar()
            if personagem.retangulo.colliderect(moeda.rect):
                moeda.coletar()
