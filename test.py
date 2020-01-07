import Reversi
import math as m
from random import randint, choice
import time
import signal, os



#returns the best move so far
def iterativeDeep(board, maxTime, turn):
    startTime = time.time()
    depth = 1
    bestMove = None
    bestVal = -9999

    try:
        TimeOut(maxTime).start()
        while True :
            move, val = explore(depth, board)
            depth += 1
            if val > bestVal :
                assert move in board.legal_moves()
                bestMove=move
                bestVal=val

    except TimeOut.TimeOutException as e :
        tkt=0


    nbW, nbB = board.get_nb_pieces()

    i = nbW+nbB
    print(board)
    while i != (turn+3):
        board.pop()
        i=i-1

    print(board)
    if bestMove not in board.legal_moves():
        print("WWWWHHHHHHHHHHHAAAAAAAAAAAAAAAAAAAAAATTTTTTTTTTTTTTTTTTTTTTππππππππππππππππp")
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

    return bestmove, best


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
    """
        TimeOut for *nix systems
    """
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

    print("tour : ", turn)
    if b.is_game_over():
        return

    if doIA:
        tour = iterativeDeep(b, 3, turn)
        print ("le tour", tour)
        b.push2(tour)

    else:
        tour = iterativeDeep(b, 1, turn)
        print ("le tour", tour)
        b.push2(tour)


    print(b)
    nbW, nbB = b.get_nb_pieces()
    print ( "et J'ai ", nbW+nbB, "pieces ")

    print("------------------------------------FIN ")
    game(b, not doIA, turn+1)



board = Reversi.Board()
game(board, 1,1)
