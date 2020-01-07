import Reversi
import math as m
from random import randint, choice

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.legal_moves()])

board_weight2 = [#8x8 => Updater
        [1000, -150, 30, 10, 10, 30, -150, 1000],
        [-150, -250, 0, 0, 0, 0, -250, -150],
        [30, 0, 1, 2, 2, 1, 0, 30],
        [10, 0, 2, 16, 16, 2, 0, 10],
        [10, 0, 2, 16, 16, 2, 0, 10],
        [30, 0, 1, 2, 2, 1, 0, 30],
        [-150, -250, 0, 0, 0, 0, -250, -150],
        [1000, -150, 30, 10, 10, 30, -150, 1000]]

board_weight = [#8x8 => Updater
        [100, -20, 10, 5, 5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [100, -20, 10, 5, 5, 10, -20, 100]]

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
        if board_weight[x][y] > max_weight :
            move = [p, x, y]
            max_weight = board_weight[x][y]
    return move

def choice_move3(moves) :
    move = [0, 0, 0]
    max_weight = -m.inf
    for (p, x, y) in moves :
        if board_weight[x][y] > max_weight :
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
                    comp += board_weight[i][j]
                elif board._board[i][j] == board._flip(player) :
                    comp += - board_weight[i][j]
        return comp

#Late game => recherche Alpha_beta avec fenetre restreinte pour identifier coup gagnant.
def heuristique3(board, player=None, method="Absolute") : #Pondérer les trois heuristiques -> attention aux intervalles de valeurs (normaliser avant avec bornes supérieures et eventuellement coefficient)
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
    
    

class MiniMax_AI():
    def __init__(self, color) :
        self.color = color

    def maximin(self, board, depth) :
        if board.is_game_over() :
            return result(board, self.color)
        if depth == 0 :
            return heuristique(board, self.color, "Positional")
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
            return heuristique(board, self.color, "Positional")
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
            return heuristique3(board, self.color, "Positional")
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
            return heuristique3(board, self.color, "Positional")
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
        move = playerA.best_move(b, 7)
        print(move)
        board.push(move)
        print(b)
        if not b.is_game_over() :
            move = playerB.best_move(b, 7)
            print(move)
            board.push(move)
            print(b)
        #input()

playerA = MiniMax_AI(Reversi.Board._BLACK)
playerB = MiniMax_AI3(Reversi.Board._WHITE)
board = Reversi.Board()
game(board, playerA, playerB)
