from source.Tela import Tela
from assets.Personagem.Personagem import *
from source.Cores import coresRGB


def main():
    """função principal do programa"""
    # cria a tela
    tela = Tela(800, 600, coresRGB["branco"])
    superficie = tela.criar_tela()

    clock = pg.time.Clock()

    # cria o personagem
    personagem = Personagem(superficie, 400, 300, 20, 20, 10, coresRGB["azul"])

    rodando = True
    while rodando:
        for event in pg.event.get():
            # sai do jogo
            if event.type == pg.QUIT:
                rodando = False

        # move o personagem
        personagem.mover()

        superficie.fill(coresRGB["branco"])
        personagem.desenhar()

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    """executa o programa"""

    pg.init()
    main()
    pg.quit()
    exit()
