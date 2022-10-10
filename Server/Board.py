import random
import string

initialPosition = ' '
defaultCodeSize = 5

def getRandomString(length):
    randomString = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return randomString

class Board:
    ipPlayer1 = ''
    ipPlayer2 = ''

    def __init__(self, ipPlayer1):
        self.board = [
            ' ', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ' 
        ]
        self.ipPlayer1 = ipPlayer1
        self.actualPlayer = ipPlayer1
        self.char = 'X'
        self.gameCode = getRandomString(defaultCodeSize)
        self.gameStatus = "Em andamento"
    
    def connectPlayer(self, ipPlayer2):
        self.ipPlayer2 = ipPlayer2

    def player(self):
        return self.actualPlayer

    def code(self):
        return self.gameCode

    def status(self):
        return self.gameStatus

    def gameInfo(self):
        msg = "Jogador 1: {}\nJogador 2: {}\nCódigo do jogo: {}\nStatus: {}".format(
            self.ipPlayer1, self.ipPlayer2, self.gameCode, self.gameStatus
        )
        return msg

    def play(self, position):
        playPosition = int(position) - 1
        self.board[playPosition] = self.char

    def changePlayer(self):
        if self.actualPlayer == self.ipPlayer1:
            self.actualPlayer = self.ipPlayer2
            self.char = 'O'
        else:
            self.actualPlayer = self.ipPlayer1
            self.char = 'X'

    def emptyPositions(self):
        positionsEmpty = self.board.count(initialPosition)
        return positionsEmpty

    def isEmptyPosition(self, position):
        checkPosition = int(position) - 1
        isEmpty = self.board[checkPosition] == initialPosition
        return isEmpty

    def toString(self):
        msg = "{}|{}|{}\n_____\n{}|{}|{}\n_____\n{}|{}|{}".format(
            self.board[0],self.board[1],self.board[2],
            self.board[3],self.board[4],self.board[5],
            self.board[6],self.board[7],self.board[8]
        )
        return msg

    def updateStatus(self):
        for i in range(0, 9, 3):
            if self.board[i] != initialPosition and self.board[i] == self.board[i + 1] and self.board[i + 1] == self.board[i + 2]:
                if self.actualPlayer == self.ipPlayer1:
                    self.gameStatus = "Vitória Jogador 1!"
                else:
                    self.gameStatus = "Vitória Jogador 2!"
                return
        
        for i in range(0, 3):
            if self.board[i] != initialPosition and self.board[0 + i] == self.board[3 + i] and self.board[3 + i] == self.board[6 + i]:
                if self.actualPlayer == self.ipPlayer1:
                    self.gameStatus = "Vitória Jogador 1!"
                else:
                    self.gameStatus = "Vitória Jogador 2!"

        if self.board[4] != initialPosition:
            if self.board[0] == self.board[4] and self.board[4] == self.board[8]:
                if self.actualPlayer == self.ipPlayer1:
                    self.gameStatus = "Vitória Jogador 1!"
                else:
                    self.gameStatus = "Vitória Jogador 2!"
                return 

            if self.board[3] == self.board[4] and self.board[4] == self.board[6]:
                if self.actualPlayer == self.ipPlayer1:
                    self.gameStatus = "Vitória Jogador 1!"
                else:
                    self.gameStatus = "Vitória Jogador 2!"
                return

        if self.emptyPositions() == 0:
            self.gameStatus = "Empate"
