from base64 import decode
from socket import *
import os
import time

serverIP = "localhost"

playerType = input(
    "Para criar um novo jogo, digite 1.\nPara conectar em um jogo, digite 2. \n:"
)

if playerType == "1":
    serverPort = 9990
    message = "CRIA_JOGO"
else:
    gameCode = input("Insira o código da partida: ")
    serverPort = 9991
    message = "CONECTA:" + gameCode

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
decodedMessage = ""
while not decodedMessage.startswith("ENCERRA_JOGO"):
    encodedMessage = message.encode()
    clientSocket.send(encodedMessage)

    modifiedMessage, serverIP = clientSocket.recvfrom(1500)
    decodedMessage = modifiedMessage.decode()

    if decodedMessage.startswith("JOGADA_LIBERADA"):
        print(decodedMessage[16:])
        playPosition = input("Jogador {} deve jogar: ".format(playerType))
        message = "JOGADA:" + playPosition
        encodedMessage = message.encode()
        clientSocket.send(encodedMessage)

        modifiedMessage, serverIP = clientSocket.recvfrom(1500)
        if "ENCERRA_JOGO" in modifiedMessage.decode():
            break

print(modifiedMessage.decode()[13:])
clientSocket.close()
