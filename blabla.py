import Reversi
import math as m
from random import randint, choice
import time
import signal, os



#returns the best move so far
def iterativeDeep(board, maxTime, turn):
    startTime = time.time()
    depth = 0
    bestMove = None
    bestVal = -9999
    moves = []

    try:
        TimeOut(maxTime).start()
        print("®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®")
        print(board.legal_moves())
        print("®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®®")

        while True :
            bestMove = explore(depth, board)
            moves.append(bestMove)
            depth += 1


    except TimeOut.TimeOutException as e :
        print (moves)


    #remise du plateau au cas où l'interuption ne l'ai pas fait
    nbW, nbB = board.get_nb_pieces()
    i = nbW+nbB
    while i != (turn+3):
        board.pop()
        i=i-1


    if bestMove not in board.legal_moves():
        print ("le coup ", bestMove)
        return choice([m for m in board.legal_moves()])

    return bestMove

#get the best move of the given depth
def explore(depth, b):
    best = -99999
    bestmove = None

    for m in b.legal_moves():
        b.push(m)
        value = minMax(board, depth ,-99999, 99999,1)
        b.pop()
        if value > best:
            best = value
            bestmove = m

    return bestmove


# def negamax(board, depth, alpha, beta):
#     if depth == 0:
#         return board.heuristique(board)
#     if board.is_game_over():
#         return board.heuristique(board)
#
#     bestValue = -9999
#     for m in board.legal_moves():
#         board.push(m)
#         bestValue = max(bestValue, -negamax(board, depth-1,  alpha, beta))
#         board.pop()
#         alpha = max(alpha, bestValue)
#
#         if alpha >= beta:
#             break
#
#         return bestValue


def minMax(b, nb, alpha, beta, isMaxP):
    if nb == 0:
        return b.heuristique(b)
    if b.is_game_over():
        return b.heuristique(b)

    if isMaxP:
        best = -99999999999
        for m in b.legal_moves():
            b.push(m)
            best = max(minMax(b, nb -1, alpha, beta, not isMaxP), best)
            b.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                return best

        return best

    else :
        best = 99999999999
        for m in b.legal_moves():
            b.push(m)
            best = min(minMax(b, nb -1, alpha, beta, not isMaxP), best)
            b.pop()
            beta = min(beta, best)
            if beta <= alpha:
                return best
        return best

class TimeOut():

    class TimeOutException(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec # time we want an exception to be raised after
        self.start_time = None # to measure actual time

    def start(self):
        self.start_time = time.time()
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def raise_timeout(self, *args):
        signal.alarm(0) # disable
        message = "Alarm set for {}s and actually passed {}s".format(self.sec,  round(time.time() - self.start_time, 5))
        raise TimeOut.TimeOutException(message)




def game2(b, playerA, playerB) :
    print(b)
    while not b.is_game_over() :
        move = playerA.iterativeDeep(b,3)
        board.push(move)
        print(b)
        if not b.is_game_over() :
            move = playerB.iterativeDeep(b, 1)
            board.push(move)
            print(b)



def game(b, doIA, turn):
    print("----------------------------------DEBUT ")

    print("coup : ", turn)
    if b.is_game_over():
        return

    if doIA:
        coup = iterativeDeep(b, 3, turn)
        print ("le coup", coup)
        b.push2(coup)

    else:
        coup = iterativeDeep(b, 1, turn)
        print ("le coup", coup)
        b.push2(coup)


    print(b)
    nbW, nbB = b.get_nb_pieces()
    print ( "je veux ", turn +4, "pieces" )
    print ( "et J'ai ", nbW+nbB, "pieces ")

    print("------------------------------------FIN ")
    game(b, not doIA, turn+1)



board = Reversi.Board()
game(board, 1,1)
