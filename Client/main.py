from base64 import decode
from socket import *
import os
import time

serverIP = "localhost"
playerType = 0
while playerType != "1" and playerType != "2":
    playerType = input(
        "Para criar um novo jogo, digite 1.\nPara conectar em um jogo, digite 2.\nPara ajuda em como jogar, digite 3. \n:"
    )
    if playerType == "1":
        serverPort = 9990
        message = "CRIA_JOGO"
    elif playerType == "2":
        gameCode = input("Insira o código da partida: ")
        serverPort = 9991
        message = "CONECTA:" + gameCode
    elif playerType == "3":
        print(
            "Na sua vez de jogar digite o número da posição que deseja jogar, de 1 a 9.\n\n1|2|3\n_____\n4|5|6\n_____\n7|8|9\n"
        )
    else:
        print("Opção inválida!")

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
decodedMessage = ""
while not decodedMessage.startswith("ENCERRA_JOGO"):

    encodedMessage = message.encode()
    clientSocket.send(encodedMessage)

    modifiedMessage, serverIP = clientSocket.recvfrom(1500)
    decodedMessage = modifiedMessage.decode()
    if decodedMessage.startswith("CODIGO_DE_ACESSO:"):
        os.system("cls" if os.name == "nt" else "clear")
        print("Código para conectar: " + decodedMessage[17:])

    if decodedMessage.startswith("JOGADA_LIBERADA"):
        os.system("cls" if os.name == "nt" else "clear")
        print(decodedMessage[:45][16:])
        playPosition = "0"
        while (
            not playPosition.isnumeric()
            or int(playPosition) < 1
            or int(playPosition) > 9
        ):
            playPosition = input("\nJogador {} deve jogar: ".format(playerType))
        message = "JOGADA:" + playPosition
        encodedMessage = message.encode()
        clientSocket.send(encodedMessage)

        modifiedMessage, serverIP = clientSocket.recvfrom(1500)

        if "ENCERRA_JOGO" in modifiedMessage.decode():
            break
    if not decodedMessage.startswith("CODIGO_DE_ACESSO:"):
        os.system("cls" if os.name == "nt" else "clear")
    if modifiedMessage.decode().startswith("JOGADA_CONFIRMADA"):
        print(modifiedMessage.decode()[:82][18:])

print(modifiedMessage.decode()[13:])
clientSocket.close()
