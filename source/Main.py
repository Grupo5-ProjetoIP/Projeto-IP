import pygame as pg
from Tela import Tela
from Personagem import *
from Cores import coresRGB
from Coletaveis import *
from Labirinto import Labirinto


class Main:
    "classe principal do programa"

    def __init__(self):
        """inicializa as variáveis do programa"""

        pg.init()

        # cria a tela
        self.tela = Tela(800, 600, coresRGB["branco"])
        self.superficie = self.tela.criar_tela()

        self.clock = pg.time.Clock()

        self.rodando = True
        self.jogando = False

    def menu_principal(self):
        """tela do menu"""

        # textos
        # titulo
        titulo = pg.font.SysFont(None, 100)
        objeto_titulo = titulo.render(
            "Cin Maze", True, coresRGB["branco"], coresRGB["vermelho"])
        titulo_rect = objeto_titulo.get_rect()
        titulo_rect.topleft = (self.superficie.get_width() / 2 - titulo_rect.width / 2,
                               70)

        # botões
        botao = pg.font.SysFont(None, 60)
        # botão iniciar
        botao_iniciar = botao.render(
            "Iniciar", True, coresRGB["branco"], coresRGB["vermelho"])
        iniciar_rect = botao_iniciar.get_rect()
        iniciar_rect.topleft = (self.superficie.get_width() / 2 - iniciar_rect.width / 2,
                                250)
        iniciar_selecao = pg.Rect(iniciar_rect.x - 25, iniciar_rect.y - 10,
                                  iniciar_rect.width + 50, iniciar_rect.height + 20)

        def interagir_botao(retangulo: pg.Rect, botao: pg.Surface, fonte: pg.font.Font) -> bool:
            """verifica se o mouse está sobre o botão e se ele foi clicado"""

            # armazena a posição do mouse
            mouse_pos = pg.mouse.get_pos()

            # verifica mouse hover e desenha o botão com o fundo
            if retangulo.collidepoint(mouse_pos):
                pg.draw.rect(self.superficie,
                             coresRGB["preto"], iniciar_selecao)
                botao = fonte.render(
                    "Iniciar", True, coresRGB["branco"], coresRGB["preto"])
                self.superficie.blit(botao, retangulo)
                return True

            else:
                pg.draw.rect(self.superficie,
                             coresRGB["vermelho"], iniciar_selecao)
                botao = fonte.render(
                    "Iniciar", True, coresRGB["branco"], coresRGB["vermelho"])
                self.superficie.blit(botao, retangulo)
                return False

        # loop do menu
        while self.rodando:
            for evento in pg.event.get():
                # sai do jogo
                if evento.type == pg.QUIT:
                    self.rodando = False
                # troca para a tela de jogo (labirinto)
                elif evento.type == pg.MOUSEBUTTONDOWN and interagir_botao(iniciar_rect, botao_iniciar, botao):
                    if evento.button == 1:
                        self.jogando = True
                        self.rodando = False

            # desenha tudo no menu
            self.superficie.fill(coresRGB["vermelho"])

            self.superficie.blit(objeto_titulo, titulo_rect)
            interagir_botao(iniciar_rect, botao_iniciar, botao)

            pg.display.flip()
            self.clock.tick(30)

    def game_loop(self):
        """loop do jogo"""

        # Objetos:
        # criando a chave
        efeito_coleta_de_keys = pygame.mixer.Sound(
            'assets/sounds/fesliyan studios_collecting _keys_opção 01.wav')
        imagem_chave = pg.image.load("assets/Coletaveis/chave.png")
        pos_x = 500
        pos_y = 230
        chave = Chave(pos_x, pos_y, self.superficie,
                      imagem_chave, efeito_coleta_de_keys)

        # criando os relogios
        efeito_coleta_de_relógios = pygame.mixer.Sound(
            'assets/sounds/orange free sounds_collecting_items_opção 04.wav')
        pos_x = 300
        pos_y = 230
        tempo = Relogio(pos_x, pos_y, self.superficie,
                        efeito_coleta_de_relógios)
        tempo = Relogio(pos_x+50, pos_y, self.superficie,
                        efeito_coleta_de_relógios)

        # criando as moedas
        efeito_coleta_de_moedas = pygame.mixer.Sound(
            'assets/sounds/freesound_collecting_coins_opção 01.wav')
        imagem_moeda = pg.image.load("assets/Coletaveis/moeda.png")
        pos_y = 230
        pos_x = 500
        for _ in range(3):
            pos_x += 70
            moeda = Moeda(pos_x, pos_y, self.superficie,
                          imagem_moeda, efeito_coleta_de_moedas)

        # cria o labirinto
        imagem_labirinto = pg.image.load("assets/imagens/fundo.png")
        paredes_labirinto = pg.image.load("assets/imagens/Labirinto.png")
        labirinto = Labirinto(
            imagem_labirinto, paredes_labirinto, self.superficie)

        # cria o personagem
        imagem_personagem = pg.image.load(
            "assets/Personagem/imagens/player.png")
        personagem = Personagem(self.superficie, labirinto.parede, labirinto.piso,
                                20, 250, 35, 35, 5, coresRGB["azul"], imagem_personagem)

        while self.jogando:
            for evento in pg.event.get():
                # sai do jogo
                if evento.type == pg.QUIT:
                    self.jogando = False

            personagem.update()

            tempo.update(personagem)
            chave.update(personagem)
            moeda.update(personagem)

            pg.display.flip()
            self.clock.tick(30)

    def update(self):
        self.menu_principal()
        self.game_loop()


if __name__ == "__main__":
    """executa o programa"""

    main = Main()
    main.update()

    pg.quit()
    exit()
