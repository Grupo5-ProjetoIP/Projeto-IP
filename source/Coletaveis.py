import pygame
import pygame as pg

pygame.init()

efeito_coleta_de_moedas = pygame.mixer.Sound('assets/sounds/freesound_collecting_coins_opção 01.wav')
efeito_coleta_de_keys = pygame.mixer.Sound('assets/sounds/fesliyan studios_collecting _keys_opção 01.wav')
efeito_coleta_de_relógios = pygame.mixer.Sound('assets/sounds/orange free sounds_collecting_items_opção 04.wav')

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

    sprite_sheet = pg.image.load("assets/Coletaveis/chave.png")

    def __init__(self, x: float, y: float, janela: pg.Surface, image: pg.Surface, altura: float = 40, largura: float = 40):
        super().__init__(x, y, janela, image)
        Chave.chave_ativa.append(self)

        self.sprites = []
        for i in range(4):
            img = Chave.sprite_sheet.subsurface((i*64,0), (64,64))
            img = pg.transform.scale(img, (largura, altura))
            self.sprites.append(img)

        self.atual = 0
        self.image = self.sprites[self.atual]

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
            if personagem.rect.colliderect(self.rect):
                self.coletar()
                efeito_coleta_de_keys.play()
        
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
            if personagem.rect.colliderect(relogio.rect):
                relogio.coletar()
                efeito_coleta_de_relógios.play()
        

class Moeda(Coletaveis):
    moedas_coletadas = 0
    moedas_ativas = []

    sprite_sheet = pg.image.load("assets/Coletaveis/moeda.png")

    def __init__(self, x: float, y: float, janela: pg.Surface, image: pg.Surface, altura: float = 40, largura: float = 40):
        super().__init__(x, y, janela, image)
        Moeda.moedas_ativas.append(self)

        self.sprites = []
        for i in range(4):
            img = Moeda.sprite_sheet.subsurface((i*64,0), (64,64))
            img = pg.transform.scale(img, (largura, altura))
            self.sprites.append(img)

        self.atual = 0
        self.image = self.sprites[self.atual]

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
            if personagem.rect.colliderect(moeda.rect):
                moeda.coletar()
                efeito_coleta_de_moedas.play()