import chess
import random

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