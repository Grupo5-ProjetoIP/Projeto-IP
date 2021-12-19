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
        self.tela = Tela(800, 700, coresRGB["branco"])
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

        # fundo
        fundo_atual = 0
        fundo_principal = pg.image.load('assets/imagens/menu.png')
        sprites_menu = []
        for i in range(4):
            img = fundo_principal.subsurface((i*800, 0), (800, 700))
            sprites_menu.append(img)

        # textos
        # botões
        botao = pg.font.SysFont(None, 60)
        # botão iniciar
        botao_iniciar = botao.render(
            "Iniciar", True, coresRGB["branco"])
        iniciar_rect = botao_iniciar.get_rect()
        iniciar_rect.topleft = (self.superficie.get_width() / 2 - iniciar_rect.width / 2,
                                450)
        selecao = pg.Surface(
            (iniciar_rect.width + 50, iniciar_rect.height + 20))
        selecao.set_alpha(128)
        selecao.fill(coresRGB["preto"])

        # botão historia
        botao_historia = botao.render(
            "Historia", True, coresRGB["branco"])
        historia_rect = botao_historia.get_rect()
        historia_rect.topleft = (self.superficie.get_width() / 2 - historia_rect.width / 2,
                                 530)

        def interagir_botao(retangulo: pg.Rect, botao: pg.Surface, fonte: pg.font.Font,
                            selecao: pg.Surface, texto: str) -> bool:
            """verifica se o mouse está sobre o botão e se ele foi clicado"""

            # armazena a posição do mouse
            mouse_pos = pg.mouse.get_pos()

            # verifica mouse hover e desenha o botão com o fundo
            if retangulo.collidepoint(mouse_pos):
                self.superficie.blit(
                    selecao, (iniciar_rect.x - 25, retangulo.y - 10))
                botao = fonte.render(
                    texto, True, coresRGB["branco"])
                self.superficie.blit(botao, retangulo)
                return True

            else:
                botao = fonte.render(
                    texto, True, coresRGB["branco"])
                self.superficie.blit(botao, retangulo)
                return False

        def tela_historia():

            fundo = pg.image.load('assets/imagens/fundo_menu.png')
            # textos
            # titulo
            titulo = pg.font.SysFont(None, 100)
            objeto_titulo = titulo.render(
                "Historia", True, coresRGB["branco"])
            titulo_rect = objeto_titulo.get_rect()
            titulo_rect.topleft = (self.superficie.get_width() / 2 - titulo_rect.width / 2,
                                   70)

            # historia
            historia = pg.font.SysFont(None, 35)

            linhas_historia = []
            with open('assets/textos/historia.txt') as file:
                for linha in file:
                    linhas_historia.append(linha.strip())
            file.close()

            obj_linhas_historia = {}
            linhas_x = []
            linhas_y = []
            linhas_tamanho = []
            linhas_altura = []
            for i in range(len(linhas_historia)):
                texto_linha = linhas_historia[i]
                objeto_linha = historia.render(
                    texto_linha, True, coresRGB["branco"])
                linha_rect = objeto_linha.get_rect()
                linha_rect.topleft = (self.superficie.get_width() / 2 - linha_rect.width / 2,
                                      170 + 28 * i)

                linhas_x.append(linha_rect.x)
                linhas_y.append(linha_rect.y)
                linhas_tamanho.append(linha_rect.width)
                linhas_altura.append(linha_rect.height)

                obj_linhas_historia[objeto_linha] = linha_rect

            fundo_historia = pg.Surface(
                (max(linhas_tamanho) + 10, max(linhas_altura) * (len(linhas_historia) + 1) + 10))
            fundo_historia.set_alpha(128)
            fundo_historia.fill(coresRGB["preto"])
            fundo_historia_topleft = (min(linhas_x) - 5, min(linhas_y) - 5)

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

                self.superficie.blit(fundo, (0, 0))

                self.superficie.blit(fundo_historia, fundo_historia_topleft)

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

                        if interagir_botao(iniciar_rect, botao_iniciar, botao, selecao, "Iniciar"):
                            # toca o som do botão
                            if self.com_som:
                                click.play()

                            self.jogando = True
                            self.rodando = False

                        elif interagir_botao(historia_rect, botao_historia, botao, selecao, "Historia"):
                            # toca o som do botão
                            if self.com_som:
                                click.play()

                            self.historia = True
                            self.rodando = False
                            tela_historia()

            # desenha tudo no menu
            self.superficie.fill(coresRGB["vermelho"])

            # animação do fundo
            fundo_atual += 0.15
            if fundo_atual >= len(sprites_menu):
                fundo_atual = 0
            img_fundo_atual = sprites_menu[int(fundo_atual)]
            self.superficie.blit(img_fundo_atual, (0, 0))

            interagir_botao(iniciar_rect, botao_iniciar,
                            botao, selecao, "Iniciar")
            interagir_botao(historia_rect, botao_historia,
                            botao, selecao, "Historia")

            pg.display.flip()
            self.clock.tick(30)

    def game_loop(self):
        """loop do jogo"""

        # definição de acordo com a dificuldade
        if self.dificuldade == "normal":
            tempo = 80
            quant_relogios = 4
            quant_moedas = 10
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

        # cria a porta
        porta = pg.image.load('assets/imagens/porta.png')
        porta_sprites = []
        for i in range(8):
            img = porta.subsurface((i*800, 0), (800, 700))
            porta_sprites.append(img)

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
            if contador_tempo.tempo < 0:

                fonte = pygame.font.SysFont(None, 20, True, False)

                mensagem = "O tempo acabou , aperte espaço para usar os seus poderes de edição de vídeo"
                mensagem2 = "e voltar no tempo para tentar novamente"
                texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
                texto_2 = fonte.render(mensagem2, True, coresRGB["branco"])
                ret_texto = texto_formatado.get_rect()
                ret_2 = texto_2.get_rect()

                self.game_over = True
                while self.game_over:
                    for event in pygame.event.get():
                        if event.type == pg.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                self.reiniciar_jogo()

                    labirinto.desenhar_labirinto()
                    self.superficie.blit(porta_sprites[0], (0, 0))

                    ret_texto.center = (390, 340)
                    ret_2.center = (390, 370)
                    self.superficie.blit(texto_formatado, ret_texto)
                    self.superficie.blit(texto_2, ret_2)
                    pygame.display.update()

            # Tela de vitoria quando o jogador estiver com a chave e colidir com a porta
            if Chave.coletou_chave and personagem.rect.colliderect(pg.Rect(370, 50, 60, 30)):

                fonte = pygame.font.SysFont(None, 20, True, False)

                mensagem = "VITÓRIA!!!! Ricardo descobriu que a sala guardava músicas secretas da banda Faringes da Paixão!!"
                mensagem2 = "(incluindo Fofolete do cão 2)"
                mensagem3 = "APERTE ESPAÇO PARA REINICIAR"
                texto1 = fonte.render(
                    mensagem, True, coresRGB["branco"])
                texto2 = fonte.render(mensagem2, True, coresRGB["branco"])
                texto3 = fonte.render(mensagem3, True, coresRGB["branco"])
                ret_texto1 = texto1.get_rect()
                ret_texto2 = texto2.get_rect()
                ret_texto3 = texto3.get_rect()

                self.vitoria = True

                porta_atual = 0
                while self.vitoria:
                    for event in pygame.event.get():
                        if event.type == pg.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                self.reiniciar_jogo()

                    labirinto.desenhar_labirinto()
                    if porta_atual < len(porta_sprites) - 1:
                        porta_atual += 0.2
                        self.superficie.blit(
                            porta_sprites[int(porta_atual)], (0, 0))
                    else:
                        self.superficie.blit(porta_sprites[-1], (0, 0))

                    self.superficie.blit(
                        personagem.sprites_cima[0], personagem.rect)
                    ret_texto1.center = (390, 340)
                    ret_texto2.center = (390, 370)
                    ret_texto3.center = (390, 400)
                    self.superficie.blit(texto1, ret_texto1)
                    self.superficie.blit(texto2, ret_texto2)
                    self.superficie.blit(texto3, ret_texto3)
                    pygame.display.update()

            labirinto.desenhar_labirinto()
            self.superficie.blit(porta_sprites[0], (0, 0))
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
