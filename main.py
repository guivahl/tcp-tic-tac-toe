from Board import Board

ipPlayer1 = '255.255.255.255'
ipPlayer2 = '0.0.0.0'

board = Board(ipPlayer1)

board.connectPlayer(ipPlayer2)

print("Jogo Iniciado!")
print("############")
print(board.gameInfo())
print("############")
print("Posições tabuleiro")
print("1|2|3\n_____\n4|5|6\n_____\n7|8|9")
print("############")

while board.emptyPositions():
    inputMsg = "Jogador {} deve jogar: ".format(board.player())

    playPosition = str(input(inputMsg))

    if board.isEmptyPosition(playPosition):
        board.play(playPosition)

        board.updateStatus()

        if board.status() != "Em andamento":
            break

        board.changePlayer()
    else:
        print("Jogada inválida!")

    print(board.toString())

print("Jogo finalizado!")
print("############")
print(board.gameInfo())
print("############")
print(board.toString())
print("############")
