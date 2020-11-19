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
def piece_type(square):
    num = chess.parse_square(square)
    piece = board.piece_at(num)
    return piece.piece_type

# Maps the type of piece to the ammount of points it corresponds too.
point_map = {chess.KING: 1000, chess.QUEEN: 9, chess.ROOK: 5, chess.KNIGHT: 3, chess.BISHOP: 3, chess.PAWN: 1}
point_map_equals = {'=Q': 9, '=R': 5, '=B': 5, '=N': 5}

def how_many_points(move,board_):
    
    '''This function takes a move and a board and returns the points developed 
    for just this move'''
    
    #obviously if the move is checkmate
    if move.find('#') != -1:
        return 99999
    
    #This is a pawn getting to the other side with taking a piece
    elif move.find('=') != -1 and move.find('x') != -1:
        cleaned_move = move.replace('+','')
        square = cleaned_move[-4]+cleaned_move[-3]
        piece = piece_type(square)
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
        cleaned_move = move.replace('+','')
        square = cleaned_move[-2]+cleaned_move[-1]
        try:
            piece = piece_type(square)
        #This exception is for the En Passant
        except:
            return 1
        points = point_map[piece]
        return points
    
    #Castling is a little better than nothing
    elif move == '0-0-0' or move == '0-0':
        return 0.5
    
    #Not taking anything is 0 points
    else:
        return 0