
import Reversi
import math as m
from random import randint, choice
import time

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.legal_moves()])


class MiniMax_AI():
    def __init__(self, color) :
        self.color = color



    def alphabeta(self, board, depth, alpha, beta,timeout):
        if time.time() > timeout:
            raise Exception("to")

        if board.is_game_over() :
            return board.heuristique(self.color)
        if depth == 0 :
            return board.heuristique(self.color)

        value = -9999
        for move in board.legal_moves() :
            board.push(move)

            try:
                value = max(value, -self.alphabeta(board, depth - 1 ,-alpha,-beta, timeout))
                board.pop()

            except:
                board.pop()
                raise Exception("notime")

            alpha = max(alpha, value)

            if alpha>=beta:
                break
        return value



    def best_move(self, board, max_depth,timeout) :
        if board.is_game_over() :
            return result(board, self.color)
        if max_depth == 0 :
            return randomMove(board)

        bm = None
        best_val = -99999


        for move in board.legal_moves() :
            board.push(move)
            try:
                val = self.alphabeta(board, max_depth -1, -99999, 999999, timeout)

                board.pop()
            except Exception:
                board.pop()
                raise Exception('no Time')

            if val > best_val :
                best_val = val
                bm = move


        return bm

    def iterativeDeep(self, board, maxTime):
        depth = 1
        bestMove = None
        bestVal = -9999
        startTime = time.time()
        timeout = startTime+maxTime
        try :
            while True :
                bestMove = self.best_move(board,depth, timeout)
                depth += 1

        except Exception as e :
            print( e )
            return bestMove


        return bestMove





def game(b, playerA, playerB) :
    print(b)
    while not b.is_game_over() :
        move = playerA.iterativeDeep(b, 1)
        board.push(move)
        print(b)
        if not b.is_game_over() :
            move = playerB.iterativeDeep(b, 2)
            board.push(move)
            print(b)

playerA = MiniMax_AI(Reversi.Board._BLACK)
playerB = MiniMax_AI(Reversi.Board._WHITE)
board = Reversi.Board()
game(board, playerA, playerB)
