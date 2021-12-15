from Tela import Tela
from Personagem import *
from Cores import coresRGB
from Coletaveis import *
from Labirinto import Labirinto


def main():
    """função principal do programa"""
    # cria a tela
    tela = Tela(800, 600, coresRGB["branco"])
    superficie = tela.criar_tela()

    clock = pg.time.Clock()

    # Objetos:
    # criando a chave
    imagem_chave = pg.image.load("assets/Coletaveis/chave.png")
    pos_x = 500
    pos_y = 230
    chave = Chave(pos_x, pos_y, superficie, imagem_chave)

    # criando os relogios
    pos_x = 300
    pos_y = 230
    tempo = Relogio(pos_x, pos_y, superficie)
    tempo = Relogio(pos_x+50, pos_y, superficie)

    # criando as moedas
    imagem_moeda = pg.image.load("assets/Coletaveis/moeda.png")
    pos_y = 230
    pos_x = 500
    for _ in range(3):
        pos_x += 70
        moeda = Moeda(pos_x, pos_y, superficie, imagem_moeda)

    imagem_labirinto = pg.image.load("assets/imagens/fundo.png")
    paredes_labirinto = pg.image.load("assets/imagens/Labirinto.png")
    labirinto = Labirinto(imagem_labirinto, paredes_labirinto, superficie)

    # cria o personagem
    imagem_personagem = pg.image.load("assets/Personagem/imagens/player.png")
    personagem = Personagem(superficie, labirinto.parede, labirinto.piso,
                            20, 250, 35, 35, 5, coresRGB["azul"], imagem_personagem)

    rodando = True
    while rodando:
        for evento in pg.event.get():
            # sai do jogo
            if evento.type == pg.QUIT:
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
