from socket import *
import time
from Board import Board

serverIP = "localhost"

serverPortPlayer1 = 9990
serverSocketPlayer1 = socket(AF_INET, SOCK_STREAM)
serverSocketPlayer1.bind((serverIP, serverPortPlayer1))

serverPortPlayer2 = 9991
serverSocketPlayer2 = socket(AF_INET, SOCK_STREAM)
serverSocketPlayer2.bind((serverIP, serverPortPlayer2))

serverSocketPlayer1.listen(1)
print("Server online!")

connectionSocketPlayer1, addrPlayer1 = serverSocketPlayer1.accept()
messagePlayer1 = connectionSocketPlayer1.recv(1500)
decodedMessagePlayer1 = messagePlayer1.decode()

if decodedMessagePlayer1 == "CRIA_JOGO":
    board = Board(str(addrPlayer1[0]) + str(addrPlayer1[1]))
    gameCode = board.code()
    print("Novo jogo criado!")
    messagePlayer1 = "Jogo criado com sucesso\n Jogador 1 conectado\n Aguardando jogador 2 se conectar"
    connectionSocketPlayer1.send(messagePlayer1.encode())
    serverSocketPlayer2.listen(1)
    print("Código da partida: " + gameCode)
    print("Aguardando jogador 2...")

    connectionSocketPlayer2, addrPlayer2 = serverSocketPlayer2.accept()
    messagePlayer2 = connectionSocketPlayer2.recv(1500)
    decodedMessagePlayer2 = messagePlayer2.decode()

    if (
        decodedMessagePlayer2.startswith("CONECTA:")
        and decodedMessagePlayer2[8:] == gameCode
    ):
        board.connectPlayer(str(addrPlayer2[0]) + str(addrPlayer2[1]))
        print("Jogador 2 conectado!")
        messagePlayer2 = "Jogador 2 conectado com sucesso"
        connectionSocketPlayer2.send(messagePlayer2.encode())

        connectionSocketPlayer1.send(("JOGADA_LIBERADA " + board.toString()).encode())
        while board.emptyPositions() and board.gameStatus == "Em andamento":
            messagePlayer1 = connectionSocketPlayer1.recv(1500)
            if messagePlayer1.decode().startswith("JOGADA:"):
                decodedMessagePlayer1 = messagePlayer1.decode()[:8][7:]
                print("Jogador 1 jogou: ", decodedMessagePlayer1)
                if board.isEmptyPosition(decodedMessagePlayer1):
                    board.play(decodedMessagePlayer1)
                    board.updateStatus()
                    board.changePlayer()
                    if board.status() != "Em andamento":
                        break
                    print(board.toString())
                connectionSocketPlayer2.send(
                    ("JOGADA_LIBERADA " + board.toString()).encode()
                )
            messagePlayer2 = connectionSocketPlayer2.recv(1500)
            if messagePlayer2.decode().startswith("JOGADA:"):
                decodedMessagePlayer2 = messagePlayer2.decode()[:8][7:]
                print("Jogador 2 jogou: ", decodedMessagePlayer2)
                if board.isEmptyPosition(decodedMessagePlayer2):
                    board.play(decodedMessagePlayer2)
                    board.updateStatus()
                    if board.status() != "Em andamento":
                        break
                    board.changePlayer()
                    print(board.toString())
                connectionSocketPlayer1.send(
                    ("JOGADA_LIBERADA " + board.toString()).encode()
                )

    connectionSocketPlayer1.send(("ENCERRA_JOGO " + board.gameStatus).encode())
    connectionSocketPlayer1.send(("ENCERRA_JOGO " + board.gameStatus).encode())
    connectionSocketPlayer2.send(("ENCERRA_JOGO " + board.gameStatus).encode())
    time.sleep(2)
    connectionSocketPlayer1.close()
    connectionSocketPlayer2.close()
    print("FIM")
