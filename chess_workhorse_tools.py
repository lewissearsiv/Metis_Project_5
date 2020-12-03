import chess
import random
import numpy as np
import pandas as pd
import tensorflow

'''These are some intro functions to get started'''
#First lets write a function that gives us every moves
def get_possible_moves(board_):
    string = str(board_.legal_moves)
    moves_section = string[string.find('(')+1:len(string)-2]
    moves = moves_section.replace(' ','')
    return moves.split(',')

# This is a function that tells the computer to make a random move
def computer_random_move(board_,moves_):
    all_moves = get_possible_moves(board_)
    move = random.choice(all_moves)
    board_.push_san(move)
    moves_.append(move)
    if board_.is_game_over():
            print('Game Over!')
            print(moves)
    return board_

#This is how you make a move and reveal a board
def my_move(move,board_,moves_):
    possible_moves = get_possible_moves(board_)
    if move not in possible_moves:
        return "Not a possible move."
    else:
        board_.push_san(move)
        moves_.append(move)
        if board_.is_game_over():
            print('Game Over!')
            print(board.result())
            print(moves)
    return board_

#Go back a move on the board and remove a move from the ledger
def go_back(board_,moves_):
    board_.pop()
    moves_.pop()
    return board_
###########################################################################

#This function analyses a move and says how many points that move is worth
def piece_type(square,board_):
    num = chess.parse_square(square)
    piece = board_.piece_at(num)
    return piece.piece_type

# Maps the type of piece to the ammount of points it corresponds too.
point_map = {chess.KING: 1000, chess.QUEEN: 90, chess.ROOK: 50, chess.KNIGHT: 30, chess.BISHOP: 30, chess.PAWN: 10}
point_map_equals = {'=Q': 90, '=R': 50, '=B': 30, '=N': 30}

def how_many_points(move,board_):
    
    '''This function takes a move and a board and returns the points developed 
    for just this move'''

    cleaned_move = move.replace('+','')
    
    #obviously if the move is checkmate
    if move.find('#') != -1:
        return 99999
    
    #This is a pawn getting to the other side with taking a piece
    elif move.find('=') != -1 and move.find('x') != -1:
        cleaned_move = move.replace('+','')
        square = cleaned_move[-4]+cleaned_move[-3]
        piece = piece_type(square,board_)
        points = point_map[piece]
        new_points_piece = point_map_equals[cleaned_move[-2]+cleaned_move[-1]]
        total_points = points + new_points_piece
        return total_points
    
    #This is a pawn getting to the other side with taking a piece
    elif move.find('=') != -1:
        cleaned_move = move.replace('+','')
        what_piece = cleaned_move[-2]+cleaned_move[-1]
        points = point_map_equals[what_piece]
        return points
    
    #If it is a take, how many points?
    elif move.find('x') != -1:
        square = cleaned_move[-2]+cleaned_move[-1]
        try:
            piece = piece_type(square,board_)
        #This exception is for the En Passant
        except:
            return 10
        points = point_map[piece]
        return points
    
    #Castling is important for long term strategies
    elif cleaned_move == '0-0-0' or cleaned_move == '0-0':
        return 4
    
    #Not taking anything is 0 points
    else:
        return 0


def how_many_points_center(move,board_):
    
    '''This function takes a move and a board and returns the points developed 
    for just this move including incentive to control the center'''
    
    #Incentivize controlling the center after the first few special cases
    center = ['e4','d4','e5','d5']
    sub_center = ['c3','d3','e3','f3','c6','d6','e6','f6','f5','f4','c5','c4']
    center_score = 0
    cleaned_move = move.replace('+','')
    
    #obviously if the move is checkmate
    if move.find('#') != -1:
        return 99999
    
    #This is a pawn getting to the other side with taking a piece
    elif move.find('=') != -1 and move.find('x') != -1:
        cleaned_move = move.replace('+','')
        square = cleaned_move[-4]+cleaned_move[-3]
        piece = piece_type(square, board_)
        points = point_map[piece]
        new_points_piece = point_map_equals[cleaned_move[-2]+cleaned_move[-1]]
        total_points = points + new_points_piece
        return total_points
    
    #This is a pawn getting to the other side with taking a piece
    elif move.find('=') != -1:
        cleaned_move = move.replace('+','')
        what_piece = cleaned_move[-2]+cleaned_move[-1]
        points = point_map_equals[what_piece]
        return points
    
    #If it is a take, how many points?
    elif move.find('x') != -1:
        square = cleaned_move[-2]+cleaned_move[-1]
        if square in center:
            center_score += 2
        if square in sub_center:
            center_score += 1
        try:
            piece = piece_type(square, board_)
        #This exception is for the En Passant
        except:
            return 10 + center_score
        points = point_map[piece]
        return points + center_score
    
    #Castling is important for long term strategies
    elif cleaned_move == '0-0-0' or cleaned_move == '0-0':
        return 4
    
    #Not taking anything is 0 points
    else:
        square = cleaned_move[-2]+cleaned_move[-1]
        if square in center:
            center_score += 2
        if square in sub_center:
            center_score += 1
        return 0 + center_score

###########################################################################
###########################################################################
#One hot encoding a board
chess_dict = {
    'p' : [1,0,0,0,0,0,0,0,0,0,0,0],
    'P' : [0,0,0,0,0,0,1,0,0,0,0,0],
    'n' : [0,1,0,0,0,0,0,0,0,0,0,0],
    'N' : [0,0,0,0,0,0,0,1,0,0,0,0],
    'b' : [0,0,1,0,0,0,0,0,0,0,0,0],
    'B' : [0,0,0,0,0,0,0,0,1,0,0,0],
    'r' : [0,0,0,1,0,0,0,0,0,0,0,0],
    'R' : [0,0,0,0,0,0,0,0,0,1,0,0],
    'q' : [0,0,0,0,1,0,0,0,0,0,0,0],
    'Q' : [0,0,0,0,0,0,0,0,0,0,1,0],
    'k' : [0,0,0,0,0,1,0,0,0,0,0,0],
    'K' : [0,0,0,0,0,0,0,0,0,0,0,1],
    '.' : [0,0,0,0,0,0,0,0,0,0,0,0],
}
alpha_dict = {
    'a' : [0,0,0,0,0,0,0],
    'b' : [1,0,0,0,0,0,0],
    'c' : [0,1,0,0,0,0,0],
    'd' : [0,0,1,0,0,0,0],
    'e' : [0,0,0,1,0,0,0],
    'f' : [0,0,0,0,1,0,0],
    'g' : [0,0,0,0,0,1,0],
    'h' : [0,0,0,0,0,0,1],
}
number_dict = {
    1 : [0,0,0,0,0,0,0],
    2 : [1,0,0,0,0,0,0],
    3 : [0,1,0,0,0,0,0],
    4 : [0,0,1,0,0,0,0],
    5 : [0,0,0,1,0,0,0],
    6 : [0,0,0,0,1,0,0],
    7 : [0,0,0,0,0,1,0],
    8 : [0,0,0,0,0,0,1],
}

def make_matrix(board): 
    fen = board.epd()
    outer_list = []  
    pieces = fen.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        inner_list = []  
        for entry in row:
            if entry.isdigit():
                for i in range(0, int(entry)):
                    inner_list.append('.')
            else:
                inner_list.append(entry)
        outer_list.append(inner_list)
    return outer_list

def translate(board, matrix,chess_dict):
    rows = []
    for row in matrix:
        terms = []
        for term in row:
            terms.append(chess_dict[term])
        rows.append(terms)
    return rows

white_to_move = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

black_to_move = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def encode_board(board_):
    encoded = translate(board_, make_matrix(board_),chess_dict)

    #This includes the turn
    if board_.turn:
        encoded.append(white_to_move)
    else:
        encoded.append(black_to_move)
    return encoded 
    

#Want to do this!!! May be too hard
def encode_move_rigorous(entry):
    try:
        term = entry
        term = term.replace('x','')
        term = term.replace('#','')
        term = term.replace('+','')
        if len(term) == 2:
            piece = 'p' 
        else:
            piece = term[0]
        alpha = term[-2]
        number = term[-1]
        return [chess_dict[piece],alpha_dict[alpha],number_dict[int(number)]]
    except:
        pass

def encode_move_easy(entry):
    if entry == 'O-O':
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if entry == 'O-O-O':
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    try:
        term = entry
        term = term.replace('x','')
        term = term.replace('#','')
        term = term.replace('+','')
        if len(term) == 2:
            piece = 'p' 
        else:
            piece = term[0]
        alpha = term[-2]
        number = term[-1]
        p = chess_dict[piece]
        a = alpha_dict[alpha]
        n = number_dict[int(number)]
        output = []
        for x in p:
            output.append(x)
        for x in a:
            output.append(x)
        for x in n:
            output.append(x)
        return output
    except:
        return 'Weird Move'

def cnn_predict(cnn_model,board_):
    encoded_board = encode_board(board_)
    board_tensor = tensorflow.expand_dims(np.array(encoded_board),0)
    prediction = cnn_model.predict(board_tensor)
    return prediction