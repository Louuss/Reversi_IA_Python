# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *
import math as m

board_weight2 = [
        [1000, -150, -50, 30, 10, 10, 30, -50, -150, 1000],
        [-150, -250, -30, 15, 5, 5, 15, -30, -250, -150],
        [-50, -30, 15, 0, 0, 0, 0, 15, -30, -50],
        [30, 15, 0, 1, 2, 2, 1, 0, 15, 30],
        [10, 5, 0, 2, 16, 16, 2, 0, 5, 10],
        [10, 5, 0, 2, 16, 16, 2, 0, 5, 10],
        [30, 15, 0, 1, 2, 2, 1, 0, 15, 30],
        [-50, -30, 15, 0, 0, 0, 0, 15, -30, -50],
        [-150, -250, -30, 15, 5, 5, 15, -30, -250, -150],
        [1000, -150, -50, 30, 10, 10, 30, -50, -150, 1000]]

def result(board, color) :
    white, black = board.get_nb_pieces()
    if color == Reversi.Board._BLACK :
        if black > white :
            return m.inf
        elif white > black:
            return -m.inf
        else :
            return 0
    elif color == Reversi.Board._WHITE :
        if white > black :
            return m.inf
        elif black > white :
            return -m.inf
        else :
            return 0

def choice_move(moves) :
    move = [0, 0, 0]
    max_weight = -m.inf
    for (p, x, y) in moves :
        if board_weight2[x][y] > max_weight :
            move = [p, x, y]
            max_weight = board_weight2[x][y]
    return move

#Late game => recherche Alpha_beta avec fenetre restreinte pour identifier coup gagnant.

def mobility(board, player) :#Mobilité immédiate, pas potentielle.
    m_player = board.count_legal_moves(player)
    m_opponent = board.count_legal_moves(board._flip(player))
    try :
        return (m_player - m_opponent) / (m_player + m_opponent)
    except :
        return 0

def absolute(board, player) :
    if player == board._WHITE :
        return (board._nbWHITE - board._nbBLACK) / (board._nbWHITE+board._nbBLACK)
    return (board._nbBLACK - board._nbWHITE) / (board._nbBLACK+board._nbWHITE)

def parity(board, player) :
    return 1 if ((board._boardsize**2)-(board._nbBLACK+board._nbWHITE)) %2 == 1 else -1

def positional(board, player) : #Modifier poids selon valeur corner
    comp = 0
    total = 0
    board_weight = board_weight2.copy()
    for (i,j) in [(0, 0), (0, board._boardsize-1), (board._boardsize-1, 0), (board._boardsize-1, board._boardsize-1)] :
        if board._board[i][j] != board._EMPTY :
            for k in range(-2, 3) :
                if i+k > 0 and i+k < board._boardsize :
                    for l in range(-2, 3) :
                        if j+l > 0 and j+l < board._boardsize :
                            board_weight[i+k][j+l] = max(0, board_weight[i+k][j+l])
    for i in range(0, board._boardsize) :
        for j in range(0, board._boardsize) :
            if board._board[i][j] == player :
                comp += board_weight[i][j]
            elif board._board[i][j] == board._flip(player) :
                comp += - board_weight2[i][j]
            total += abs(board_weight[i][j])
    return comp/total

def corner(board, player) :
    c_player = board.count_corner(player)
    c_opponent = board.count_corner(board._flip(player))
    try :
        #print(c_player, c_opponent, (c_player - c_opponent) / (c_player + c_opponent))
        return (c_player - c_opponent) / (c_player + c_opponent)
    except Exception as err:
        return 0

#Stabilité? Chaud ><'

#Late game => recherche Alpha_beta avec fenetre restreinte pour identifier coup gagnant.
def heuristique(board, player=None, phase = 0) : #Pondérer les trois heuristiques -> attention aux intervalles de valeurs (normaliser avant avec bornes supérieures et eventuellement coefficient)
    a = absolute(board, player)
    w = positional(board, player)
    c = corner(board, player)
    m = mobility(board, player)
    p = parity(board, player)
    if phase == 0 : #Early Game
        return 50 * w + 50 * m + 10000*c
    if phase == 1 : #Middle Game
        return 20 * w + 10 * m + 20 * a + 50 * p + 10000*c
    if phase == 2 : #Late Game
        return 100*a + 100 * p + 10000*c

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._color = None
        self._timer = 295 #Buffer de sécurité

    def getPlayerName(self):
        return "Verecti"

    def alphaBetaMin(self, depth, alpha, beta, timeout=m.inf) :
        if time.time() > timeout:
            raise Exception("to")

        if self._board.is_game_over() :
            return result(self._board, self._color)
        if depth == 0 :
            if (self._board._nbWHITE + self._board._nbBLACK) < 25 :
                return heuristique(self._board, self._color, 0)
            if (self._board._nbWHITE + self._board._nbBLACK) < 90 and (self._board.count_corner(self._board._WHITE)+self._board.count_corner(self._board._BLACK)) < 4 :
                return heuristique(self._board, self._color, 1)
            return heuristique(self._board, self._color, 2)
        
        for move in self._board.legal_moves() :
            self._board.push(move)

            try:
                beta = min(beta, self.alphaBetaMax(depth - 1 , alpha, beta, timeout))
                self._board.pop()

            except:
                self._board.pop()
                raise Exception("notime")
            
            if alpha>=beta:
                break
        return beta

    def alphaBetaMax(self, depth, alpha, beta, timeout=m.inf) :
        if time.time() > timeout:
            raise Exception("to")

        if self._board.is_game_over() :
            return result(self._board, self._color)
        if depth == 0 :
            if (self._board._nbWHITE + self._board._nbBLACK) < 25 :
                return heuristique(self._board, self._color, 0)
            if (self._board._nbWHITE + self._board._nbBLACK) < 90 and (self._board.count_corner(self._board._WHITE)+self._board.count_corner(self._board._BLACK)) < 4 :
                return heuristique(self._board, self._color, 1)
            return heuristique(self._board, self._color, 2)
        
        for move in self._board.legal_moves() :
            self._board.push(move)

            try:
                alpha = max(alpha, self.alphaBetaMin(depth - 1 , alpha, beta, timeout))
                self._board.pop()

            except:
                self._board.pop()
                raise Exception("notime")
            
            if alpha>=beta:
                break
        return alpha

    def iterativeDeep(self, maxTime, alpha = -m.inf, beta = m.inf):
        depth = 1
        bestMove = None
        bestVal = -m.inf
        startTime = time.time()
        timeout = startTime+maxTime
        print(timeout, startTime)
        try :
            while True :
                bestMove = self.bestMove(depth, timeout, alpha=-m.inf, beta = m.inf)
                depth += 1

        except Exception as e :
            print( e )
            return bestMove
        
        return bestMove

    def bestMove(self, max_depth,timeout=m.inf, alpha = -m.inf, beta = m.inf) :
        if self._board.is_game_over() :
            return result(board, self.color)
        if max_depth == 0 :
            return randomMove(board)

        best_move = []
        best_val = -m.inf


        for move in self._board.legal_moves() :
            self._board.push(move)
            try:
                val = self.alphaBetaMin(max_depth -1, alpha, beta, timeout)
                self._board.pop()
            except Exception:
                self._board.pop()
                raise Exception('no Time')

            if val > best_val :
                best_val = val
                best_move = [move]
            elif val == best_val :
                best_move.append(move)

        return choice_move(best_move)

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        ####
        """if self._color == self._board._BLACK :
            move = self.bestMove(3)#Test
        else :
            move = self.bestMove(4)
        self._board.push(move)"""
        currentTime = time.time()
        if (self._board._nbWHITE + self._board._nbBLACK) < 25 : #Early game
            move = self.iterativeDeep(3)
        elif (self._board._nbWHITE + self._board._nbBLACK) < 90 and (self._board.count_corner(self._board._WHITE)+self._board.count_corner(self._board._BLACK)) < 4 :#Middle game
            move = self.iterativeDeep(6)
        else :
            if ((self._board._nbWHITE + self._board._nbBLACK) < 90) : #Early Late Game
                move = self.iterativeDeep(7)
            else : #Late late game
                move = self.iterativeDeep(1, alpha=0, beta = 999999999)
                if move == None :
                    move = self.iterativeDeep(4)
                    #Check if dangerous further away?
        self._timer -= time.time() - currentTime
        print("Time spent : ", time.time() - currentTime)
        self._board.push(move)
        """
        depth = 3 => ~40s, depth = 4 => ~377s (Invalide car > 300s)
        TODO : Algorithme (cf heuristique pour phases)
        Early game => depth 3, 3s max : garanti finition
        Middle game => depth 4, 6-7s : risque de ne pas finir, à observer
        Early Late game (> 10 tours restant) => same as Middle Game? -> peut être passer en depth 3 si pb.
        Late game (<= 10 tours restant) => 2s alpha beta dectectant coup gagnant, 3s en depth3 si rien trouvé.
        """
        ####
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._color)
        print("My current board :")
        print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._color = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._color == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



