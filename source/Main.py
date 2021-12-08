from source.Tela import *
from assets.Personagem.Personagem import *
from source.Cores import coresRGB


def main():
    """função principal do programa"""
    # cria a tela
    largura = 800
    altura = 600
    tela = criar_tela(largura, altura, coresRGB["branco"])

    clock = pg.time.Clock()

    # cria o personagem
    personagem = Personagem(tela, 400, 300, 20, 20, 10, coresRGB["azul"])

    rodando = True
    while rodando:
        for event in pg.event.get():
            # sai do jogo
            if event.type == pg.QUIT:
                rodando = False

        # move o personagem
        personagem.mover()

        tela.fill(coresRGB["branco"])
        personagem.desenhar()

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    """executa o programa"""

    pg.init()
    main()
    pg.quit()
    exit()
