import Reversi
import math as m
from random import randint, choice

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.legal_moves()])

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

board_weight5 = [
        [1000, -150, 50, 30, 10, 10, 30, 50, -150, 1000],
        [-150, -250, 30, 15, 5, 5, 15, 30, -250, -150],
        [50, 30, 15, 0, 0, 0, 0, 15, 30, 50],
        [30, 15, 0, 1, 2, 2, 1, 0, 15, 30],
        [10, 5, 0, 2, 16, 16, 2, 0, 5, 10],
        [10, 5, 0, 2, 16, 16, 2, 0, 5, 10],
        [30, 15, 0, 1, 2, 2, 1, 0, 15, 30],
        [50, 30, 20, 0, 0, 0, 0, 15, 30, 50],
        [-150, -250, 30, 15, 5, 5, 15, 30, -250, -150],
        [1000, -150, 50, 30, 10, 10, 30, 50, -150, 1000]]

print(board_weight2)


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
    else :
        print("???????")
        input()

def choice_move(moves) :
    move = [0, 0, 0]
    max_weight = -m.inf
    for (p, x, y) in moves :
        if board_weight2[x][y] > max_weight :
            move = [p, x, y]
            max_weight = board_weight2[x][y]
    return move

def choice_move3(moves) :
    move = [0, 0, 0]
    max_weight = -m.inf
    for (p, x, y) in moves :
        if board_weight2[x][y] > max_weight :
            move = [p, x, y]
            max_weight = board_weight2[x][y]
    return move

#Late game => recherche Alpha_beta avec fenetre restreinte pour identifier coup gagnant.
def heuristique(board, player=None, method="Absolute") : #Pondérer les trois heuristiques -> attention aux intervalles de valeurs (normaliser avant avec bornes supérieures et eventuellement coefficient)
    if method == "Absolute" :
        if player is board._WHITE:
            return board._nbWHITE - board._nbBLACK
        return board._nbBLACK - board._nbWHITE
    elif method == "Mobility" :
        m_player = board.count_legal_moves(player)
        m_opponent = board.count_legal_moves(board._flip(player))
        c_player = board.count_corner(player)
        c_opponent = board.count_corner(board._flip(player))
        return 10 * (c_player - c_opponent) + ((m_player - m_opponent) / (m_player + m_opponent))
    elif method == "Positional" :
        comp = 0
        for i in range(0, board._boardsize) :
            for j in range(0, board._boardsize) :
                if board._board[i][j] == player :
                    comp += board_weight2[i][j]
                elif board._board[i][j] == board._flip(player) :
                    comp += - board_weight2[i][j]
        return comp
    elif method == "Corner" :
        return corner(board, player)

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
def heuristique_up(board, player=None, phase = 0) : #Pondérer les trois heuristiques -> attention aux intervalles de valeurs (normaliser avant avec bornes supérieures et eventuellement coefficient)
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

def heuristique2(board, player=None) : #Pondérer les trois heuristiques -> attention aux intervalles de valeurs (normaliser avant avec bornes supérieures et eventuellement coefficient)
    absolute = 0
    mobility = 0
    positional = 0
    if player is board._WHITE:
        absolute = board._nbWHITE - board._nbBLACK
    else: 
        absolute =  board._nbBLACK - board._nbWHITE
    m_player = board.count_legal_moves(player)
    m_opponent = board.count_legal_moves(board._flip(player))
    c_player = board.count_corner(player)
    c_opponent = board.count_corner(board._flip(player))
    mobility = 10 * (c_player - c_opponent) + ((m_player - m_opponent) / (m_player + m_opponent))#WTH??
    for i in range(0, board._boardsize) :
        for j in range(0, board._boardsize) :
            if board._board[i][j] == player :
                positional += board_weight[i][j]
            elif board._board[i][j] == board._flip(player) :
                positional += - board_weight[i][j]
    alpha = (board._boardsize**2 - (board._nbBLACK + board._nbWHITE)) / board._boardsize**2
    beta = 1 - alpha
    #print(alpha, beta)
    return alpha / 2 * (mobility / 20 + positional / 20) + beta * (2 * absolute / board._boardsize**2)
    
class Random_AI() :
    def __init__(self, color) :
        self.color = color

    def best_move(self, board, max_depth) :
        if board.is_game_over() :
            return result(board, self.color)
        return randomMove(board)

class MiniMax_AI():
    def __init__(self, color, strat) :
        self.color = color
        self.strat = strat

    def maximin(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique(board, self.color, self.strat)
        maxi = - m.inf
        for move in board.legal_moves() :
            board.push(move)
            val = self.minimax(board, depth-1)
            board.pop()
            if val > maxi :
                maxi = val
        return maxi

    def minimax(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique(board, self.color, self.strat)
        mini = m.inf
        for move in board.legal_moves() :
            board.push(move)
            val = self.maximin(board, depth-1)
            board.pop()
            if val < mini :
                mini = val
        return mini

    def best_move(self, board, max_depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if max_depth == 0 :
            return randomMove(board)

        best_move = []
        best_val = -m.inf
        depth = max_depth
        for move in board.legal_moves() :
            board.push(move)
            val = self.minimax(board, depth-1)
            print("Move", move, " =", val)
            board.pop()
            if val > best_val :
                best_val = val
                best_move = [move]
            elif val == best_val :
                best_move.append(move)
        print("Best found move :", best_move, ", score =", best_val)
        return choice_move(best_move)

class MiniMax_AI2():
    def __init__(self, color) :
        self.color = color

    def maximin(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique2(board, self.color)
        maxi = - m.inf
        for move in board.legal_moves() :
            board.push(move)
            val = self.minimax(board, depth-1)
            board.pop()
            if val > maxi :
                maxi = val
        return maxi

    def minimax(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique2(board, self.color)
        mini = m.inf
        for move in board.legal_moves() :
            board.push(move)
            val = self.maximin(board, depth-1)
            board.pop()
            if val < mini :
                mini = val
        return mini

    def best_move(self, board, max_depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if max_depth == 0 :
            return randomMove(board)

        best_move = []
        best_val = -m.inf
        depth = max_depth
        for move in board.legal_moves() :
            board.push(move)
            val = self.minimax(board, depth-1)
            print("Move", move, " =", val)
            board.pop()
            if val > best_val :
                best_val = val
                best_move = [move]
            elif val == best_val :
                best_move.append(move)
        print("Best found move :", best_move, ", score =", best_val)
        return choice_move(best_move)

class MiniMax_AI3():
    def __init__(self, color) :
        self.color = color

    def maximin(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique_up(board, self.color)
        maxi = - m.inf
        for move in board.legal_moves() :
            board.push(move)
            val = self.minimax(board, depth-1)
            board.pop()
            if val > maxi :
                maxi = val
        return maxi

    def minimax(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            if (board._nbWHITE + board._nbBLACK) < 25 :
                return heuristique_up(board, self.color, 0)
            if (board._nbWHITE + board._nbBLACK) < 90 and (board.count_corner(board._WHITE)+board.count_corner(board._BLACK)) < 4 :
                return heuristique_up(board, self.color, 1)
            return heuristique_up(board, self.color, 2)
        mini = m.inf
        for move in board.legal_moves() :
            board.push(move)
            val = self.maximin(board, depth-1)
            board.pop()
            if val < mini :
                mini = val
        return mini

    def best_move(self, board, max_depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if max_depth == 0 :
            return randomMove(board)

        best_move = []
        best_val = -m.inf
        depth = max_depth
        for move in board.legal_moves() :
            board.push(move)
            val = self.minimax(board, depth-1)
            print("Move", move, " =", val)
            board.pop()
            if val > best_val :
                best_val = val
                best_move = [move]
            elif val == best_val :
                best_move.append(move)
        print("Best found move :", best_move, ", score =", best_val)
        return choice_move3(best_move)

class AlphaBeta_AI():
    def __init__(self, color) :
        self.color = color


    def alphabeta(self, board, depth, alpha, beta):
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique(board, self.color)

        value = -9999
        for move in board.legal_moves() :
            board.push(move)
            value = max(value, -self.alphabeta(board, depth-1,-alpha,-beta))
            board.pop()
            alpha = max(alpha, value)

            if alpha>=beta:
                break
        return value


    def best_move(self, board, max_depth) :
        print(self.color)
        if board.is_game_over() :
            return result(board, self.color)
        if max_depth == 0 :
            return randomMove(board)

        best_move = []
        best_val = -99999
        depth = max_depth
        for move in board.legal_moves() :
            board.push(move)
            val = self.alphabeta(board, depth-1, -99999, 999999)
            board.pop()
            if val > best_val :
                best_val = val
                best_move = [move]
            elif val == best_val :
                best_move.append(move)
        print("Best found move :", best_move, ", score =", best_val)
        return choice(best_move)


#Ne JAMAIS donner une profondeur paire : cela indique que l'adversaire est le dernier à jouer, et nique complètement l'heuristique Absolue ><
def game(b, playerA, playerB) :
    print(b)
    while not b.is_game_over() :
        move = playerA.best_move(b, 3)
        print(move)
        board.push(move)
        print(b)
        if not b.is_game_over() :
            move = playerB.best_move(b,3)
            print(move)
            board.push(move)
            print(b)
        #input()

playerA = Random_AI(Reversi.Board._BLACK)
playerB = MiniMax_AI3(Reversi.Board._WHITE)
board = Reversi.Board()
game(board, playerA, playerB)
