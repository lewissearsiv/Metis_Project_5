import chess 
import random
from chess_workhorse_tools import *

'''This files gives chess functions with static depth of 1, 2, and 3. Obviously, with each increase in depth
The computer gets better.'''


def computer_move_depth_1(board_,moves_):
    '''This function tells the computer to make a move just maximizing how many
    points it can get that move. Aka, we go depth 1'''    
    
    all_moves = get_possible_moves(board_)
    points_per_move = [how_many_points(move,board_) for move in all_moves]
    
    #All Zero
    if max(points_per_move) == 0:
        move = random.choice(all_moves)
        board_.push_san(move)
        moves_.append(move)
        if board_.is_game_over():
            print('Game Over!')
            print(moves_)
        return board_ 
    
    else:
        indices = [i for i, value in enumerate(points_per_move) if value == max(points_per_move)]
        max_value_moves = [all_moves[ind] for ind in indices]
        move = random.choice(max_value_moves)
        board_.push_san(move)
        moves_.append(move)
        if board_.is_game_over():
            print('Game Over!')
            print(board_.result())
            print(moves_)
        return board_ 
    
def computer_move_depth_2(board_,moves_):
    
    #Extract the state of the board
    board_state = board_.fen()
    
    #Extract all possible moves
    all_moves = get_possible_moves(board_)
    
    #This will hold net points per move
    move_points = []
    
    for move in all_moves:
        
        # reset the board
        
        #We will keep a counter of net points. This will be minimized.
        net_points = 0
        first_move_points = how_many_points(move, board_)
        
        #Now make the move and calculate the max points for the next move
        board_.push_san(move)
        all_moves_depth_2 = get_possible_moves(board_)
        points = [how_many_points(new_move,board_) for new_move in all_moves_depth_2]
        
        #Aggregate points change
        net_points = first_move_points - max(points)
        move_points.append(net_points)
        
        #revert board
        board_.pop()
        
    
    #Make the move here
    max_indices = [i for i, val in enumerate(move_points) if val == max(move_points)]
    best_moves = [all_moves[i] for i in max_indices]
    final_move = random.choice(best_moves)
    board_.push_san(final_move)
    moves_.append(final_move)
    if board_.is_game_over():
        print('Game Over!')
        print(board_.result())
        print(moves_)
    return board_

def computer_move_depth_3(board_,moves_):

    
    #Extract all possible moves at depth one
    all_moves_depth_1 = get_possible_moves(board_)

    #This will hold net points per move
    move_points = []
    
    for move_1 in all_moves_depth_1:
        
        if move_1.find('#') != -1:
            board_.push_san(move_1)
            moves_.append(move_1)
            print('Game Over!')
            print(board_.result())
            print(moves_)
            return board_
        
        #This is the points from the initial move
        first_move_points = how_many_points(move_1, board_)
        
        #Now make the move and calculate the max points for the next two moves
        board_.push_san(move_1)
        all_moves_depth_2 = get_possible_moves(board_)
        if board_.is_game_over():
            print('Game Over!')
            print(board_.result())
            print(moves_)
            return board_
        
        
        #This quantify's the response to all moves
        response_move_points = []
        for move_2 in all_moves_depth_2:
            second_move_points = how_many_points(move_2, board_)
            board_.push_san(move_2)
            all_moves_depth_3 = get_possible_moves(board_)
            points_3 = [how_many_points(new_move,board_) for new_move in all_moves_depth_3]
            response_move_points.append(second_move_points - max(points_3))
            #revert board
            board_.pop()
        
        #Aggregate points change for current move
        retaliation_points = max(response_move_points)
        net_points = first_move_points - retaliation_points
        move_points.append(net_points)
        #revert board
        board_.pop()
        
    
    #Make the move here
    max_indices = [i for i, val in enumerate(move_points) if val == max(move_points)]
    best_moves = [all_moves_depth_1[i] for i in max_indices]
    final_move = random.choice(best_moves)
    board_.push_san(final_move)
    moves_.append(final_move)
    if board_.is_game_over():
        print('Game Over!')
        print(board_.result())
        print(moves_)
    return board_