import pygame
import pygame as pg
from pygame import image
from Tela import Tela
from Personagem import *
from Cores import coresRGB
from Coletaveis import *
from Labirinto import Labirinto
from Contador import Contador
from random import choice


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
        self.historia = False
        self.jogando = False

        self.dificuldade = "normal"

        self.com_som = True

        self.spawns = [(104, 567), (767, 567),
                       (335, 567), (286, 506),
                       (342, 506), (225, 443),
                       (631, 386), (566, 382),
                       (400, 390), (165, 390),
                       (100, 390), (296, 336),
                       (565, 327), (354, 276),
                       (416, 276), (641, 265),
                       (648, 210), (355, 216),
                       (230, 216), (100, 216),
                       (405, 155), (466, 155),
                       (707, 52), (574, 95),
                       (156, 92), (335, 36)]

        self.game_over = False
        self.vitoria = False

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

        # botão historia
        botao_historia = botao.render(
            "Historia", True, coresRGB["branco"], coresRGB["vermelho"])
        historia_rect = botao_historia.get_rect()
        historia_rect.topleft = (self.superficie.get_width() / 2 - historia_rect.width / 2,
                                 330)
        historia_selecao = pg.Rect(iniciar_rect.x - 25, historia_rect.y - 10,
                                   iniciar_rect.width + 50, iniciar_rect.height + 20)

        def interagir_botao(retangulo: pg.Rect, botao: pg.Surface, fonte: pg.font.Font, selecao: pg.Rect, texto: str) -> bool:
            """verifica se o mouse está sobre o botão e se ele foi clicado"""

            # armazena a posição do mouse
            mouse_pos = pg.mouse.get_pos()

            # verifica mouse hover e desenha o botão com o fundo
            if retangulo.collidepoint(mouse_pos):
                pg.draw.rect(self.superficie,
                             coresRGB["preto"], selecao)
                botao = fonte.render(
                    texto, True, coresRGB["branco"], coresRGB["preto"])
                self.superficie.blit(botao, retangulo)
                return True

            else:
                pg.draw.rect(self.superficie,
                             coresRGB["vermelho"], selecao)
                botao = fonte.render(
                    texto, True, coresRGB["branco"], coresRGB["vermelho"])
                self.superficie.blit(botao, retangulo)
                return False

        def tela_historia():
            # textos
            # titulo
            titulo = pg.font.SysFont(None, 100)
            objeto_titulo = titulo.render(
                "Historia", True, coresRGB["branco"], coresRGB["vermelho"])
            titulo_rect = objeto_titulo.get_rect()
            titulo_rect.topleft = (self.superficie.get_width() / 2 - titulo_rect.width / 2,
                                   70)

            # historia
            historia = pg.font.SysFont("arial", 20)

            linhas_historia = []
            with open('assets/textos/historia.txt') as file:
                for linha in file:
                    linhas_historia.append(linha.strip())
            file.close()

            obj_linhas_historia = {}
            for i in range(8):
                texto_linha = linhas_historia[i]
                objeto_linha = historia.render(
                    texto_linha, True, coresRGB["branco"], coresRGB["vermelho"])
                linha_rect = objeto_linha.get_rect()
                linha_rect.topleft = (self.superficie.get_width() / 2 - linha_rect.width / 2,
                                      200 + 25 * i)

                obj_linhas_historia[objeto_linha] = linha_rect

            while self.historia:
                for evento in pg.event.get():
                    # sai do jogo
                    if evento.type == pg.QUIT:
                        self.historia = False
                        self.rodando = False
                    elif evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                        self.historia = False
                        self.rodando = True

                # desenha tudo na tela
                self.superficie.fill(coresRGB["vermelho"])

                self.superficie.blit(objeto_titulo, titulo_rect)

                for linha in obj_linhas_historia.keys():
                    self.superficie.blit(linha, obj_linhas_historia[linha])

                pg.display.flip()
                self.clock.tick(30)

        # loop do menu
        while self.rodando:
            for evento in pg.event.get():
                # sai do jogo
                if evento.type == pg.QUIT:
                    self.rodando = False
                # troca para a tela de jogo (labirinto)
                elif evento.type == pg.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        # evita o bug do pygame com som
                        try:
                            click = pygame.mixer.Sound(
                                'assets/sounds/button_sound.wav')
                        except pygame.error:
                            self.com_som = False

                        if interagir_botao(iniciar_rect, botao_iniciar, botao, iniciar_selecao, "Iniciar"):
                            # toca o som do botão
                            if self.com_som:
                                click.play()

                            self.jogando = True
                            self.rodando = False

                        elif interagir_botao(historia_rect, botao_historia, botao, historia_selecao, "Historia"):
                            # toca o som do botão
                            if self.com_som:
                                click.play()

                            self.historia = True
                            self.rodando = False
                            tela_historia()

            # desenha tudo no menu
            self.superficie.fill(coresRGB["vermelho"])

            self.superficie.blit(objeto_titulo, titulo_rect)
            interagir_botao(iniciar_rect, botao_iniciar,
                            botao, iniciar_selecao, "Iniciar")
            interagir_botao(historia_rect, botao_historia,
                            botao, historia_selecao, "Historia")

            pg.display.flip()
            self.clock.tick(30)

    def game_loop(self):
        """loop do jogo"""

        # definição de acordo com a dificuldade
        if self.dificuldade == "normal":
            tempo = 80
            quant_relogios = 4
            quant_moedas = 1
            tempo_bonus = 8

        # Objetos:
        # criando contador de tempo
        contador_tempo = Contador(self.superficie, tempo, tempo_bonus)

        # criando a chave
        offset = -32

        # evita o erro do pygame com sons
        try:
            efeito_coleta_de_keys = pygame.mixer.Sound(
                'assets/sounds/key_sound.wav')
        except pygame.error:
            self.com_som = False

        imagem_chave = pg.image.load("assets/Coletaveis/chave.png")
        pos_x, pos_y = choice(self.spawns)
        self.spawns.remove((pos_x, pos_y))
        pos_x += offset
        pos_y += offset

        if self.com_som:
            chave = Chave(pos_x, pos_y, self.superficie,
                          efeito_coleta_de_keys)
        else:
            chave = Chave(pos_x, pos_y, self.superficie)

        # criando os relogios
        offset = -20

        # evita o erro do pygame com sons
        try:
            efeito_coleta_de_relogios = pygame.mixer.Sound(
                'assets/sounds/clock_sound.wav')
        except pygame.error:
            self.com_som = False

        for _ in range(quant_relogios):
            pos_x, pos_y = choice(self.spawns)
            self.spawns.remove((pos_x, pos_y))
            pos_x += offset
            pos_y += offset

            if self.com_som:
                relogio = Relogio(pos_x, pos_y, self.superficie,
                                  contador_tempo, efeito_coleta_de_relogios, tempo_extra=tempo_bonus)
            else:
                relogio = Relogio(pos_x, pos_y, self.superficie,
                                  contador_tempo, tempo_extra=tempo_bonus)

        # criando as moedas
        offset = -32

        # evita o bug do pygame com sons
        try:
            efeito_coleta_de_moedas = pygame.mixer.Sound(
                'assets/sounds/coin_sound.wav')
        except pygame.error:
            self.com_som = False

        imagem_moeda = pg.image.load("assets/Coletaveis/moeda.png")
        for _ in range(quant_moedas):
            pos_x, pos_y = choice(self.spawns)
            self.spawns.remove((pos_x, pos_y))
            pos_x += offset
            pos_y += offset

            if self.com_som:
                moeda = Moeda(pos_x, pos_y, self.superficie,
                              efeito_coleta_de_moedas)
            else:
                moeda = Moeda(pos_x, pos_y, self.superficie)

        contador_coletaveis = ContadorColetaveis(self.superficie)

        # cria o labirinto
        imagem_labirinto = pg.image.load("assets/imagens/fundo.png")
        paredes_labirinto = pg.image.load("assets/imagens/Labirinto.png")
        labirinto = Labirinto(
            imagem_labirinto, paredes_labirinto, self.superficie)

        # cria o personagem
        imagem_personagem = pg.image.load(
            "assets/Personagem/imagens/player.png")
        personagem = Personagem(self.superficie, labirinto.parede, labirinto.piso,
                                385, 550, 35, 35, 5, coresRGB["azul"], imagem_personagem)

        while self.jogando:
            for evento in pg.event.get():
                # sai do jogo
                if evento.type == pg.QUIT:
                    self.jogando = False

            # Game over quando o tempo acabar
            if contador_tempo.tempo <= 0:

                fonte = pygame.font.SysFont(None, 20, True, False)

                mensagem = "aperte espaço para usar os seus poderes de edição de vídeo e voltar no tempo para tentar novamente"
                texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
                ret_texto = texto_formatado.get_rect()

                self.game_over = True
                while self.game_over:
                    self.superficie.fill((0, 0, 0))
                    for event in pygame.event.get():
                        if event.type == pg.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                self.reiniciar_jogo()

                    ret_texto.center = (390, 340)
                    self.superficie.blit(texto_formatado, ret_texto)
                    pygame.display.update()

            # Tela de vitoria quando o jogador estiver com a chave e colidir com a porta
            if Chave.coletou_chave:
                if personagem.rect.colliderect(pg.Rect(370, 50, 60, 30)):
                    fonte = pygame.font.SysFont(None, 20, True, False)

                    mensagem = "VITÓRIA!!!! APERTE ESPAÇO PARA JOGAR NOVAMENTE"
                    texto_formatado = fonte.render(
                        mensagem, True, (255, 255, 255))
                    ret_texto = texto_formatado.get_rect()

                    self.vitoria = True
                    while self.vitoria:
                        self.superficie.fill((0, 0, 0))
                        for event in pygame.event.get():
                            if event.type == pg.QUIT:
                                pygame.quit()
                                exit()
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_SPACE:
                                    self.reiniciar_jogo()
                        ret_texto.center = (390, 340)
                        self.superficie.blit(texto_formatado, ret_texto)
                        pygame.display.update()

            labirinto.desenhar_labirinto()
            personagem.update()
            contador_tempo.update()

            relogio.update(personagem)
            moeda.update(personagem)
            contador_coletaveis.update()

            if moeda.moedas_coletadas == quant_moedas:
                chave.update(personagem)

            pg.display.flip()
            self.clock.tick(30)

    def reiniciar_jogo(self):
        Moeda.moedas_coletadas = 0
        Moeda.moedas_ativas = []
        Chave.coletou_chave = False
        Relogio.tempos_ativos = []
        self.game_over = False
        self.__init__()
        self.rodando = False
        self.jogando = True
        self.update()

    def update(self):
        self.menu_principal()
        self.game_loop()


if __name__ == "__main__":
    """executa o programa"""

    main = Main()
    main.update()

    pg.quit()
    exit()
