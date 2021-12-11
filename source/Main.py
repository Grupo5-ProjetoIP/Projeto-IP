from Tela import Tela
from Personagem import *
from Cores import coresRGB


def main():
    """função principal do programa"""
    # cria a tela
    tela = Tela(800, 600, coresRGB["branco"])
    superficie = tela.criar_tela()

    clock = pg.time.Clock()

    imagem_labirinto = pg.image.load("assets/imagens/teste_colisao.png")
    labirinto = pg.sprite.Sprite()
    labirinto.rect = imagem_labirinto.get_rect()
    labirinto.image = pg.transform.scale(imagem_labirinto, (800, 600))

    # cria o personagem
    imagem_personagem = pg.image.load("assets/Personagem/imagens/teste.png")
    personagem = Personagem(superficie, labirinto,
                            20, 230, 40, 40, 10, coresRGB["azul"], imagem_personagem)

    rodando = True
    while rodando:
        for event in pg.event.get():
            # sai do jogo
            if event.type == pg.QUIT:
                rodando = False

        personagem.update()

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    """executa o programa"""

    pg.init()
    main()
    pg.quit()
    exit()
