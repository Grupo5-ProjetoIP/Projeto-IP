from Tela import Tela
from Personagem import *
from Cores import coresRGB
from Coletaveis import *


def main():
    """função principal do programa"""
    # cria a tela
    tela = Tela(800, 600, coresRGB["branco"])
    superficie = tela.criar_tela()

    clock = pg.time.Clock()

    # Objetos:
    # criando a chave
    imagem_chave = pg.image.load("assets/Coletaveis/chaves.png")
    pos_x = 500
    pos_y = 200
    chave = Chave(pos_x, pos_y, superficie, imagem_chave)

    # criando os relogios
    pos_x = 55
    pos_y = 70
    tempo = Relogio(pos_x, pos_y, superficie )
    tempo = Relogio(pos_x+50, pos_y, superficie)

    # criando as moedas
    imagem_moeda = pg.image.load("assets/Coletaveis/moeda.png")
    pos_y = 70
    pos_x = 300
    for _ in range(3):
        moeda = Moeda(pos_x, pos_y, superficie, imagem_moeda)
        pos_y += 100


    # cria o personagem
    imagem_personagem = pg.image.load("assets/Personagem/imagens/teste.png")
    personagem = Personagem(superficie, 400, 300, 40,
                            40, 10, coresRGB["azul"], imagem_personagem)

    rodando = True
    while rodando:
        for event in pg.event.get():
            # sai do jogo
            if event.type == pg.QUIT:
                rodando = False

        personagem.update()

        tempo.update(personagem)
        chave.update(personagem)
        moeda.update(personagem)

        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    """executa o programa"""

    pg.init()
    main()
    pg.quit()
    exit()
