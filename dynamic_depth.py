import chess
import random
import numpy as np
import pandas as pd
from chess_workhorse_tools import *

def n_deep_nested(board_,n):
    '''Takes a board and returns all possible move combinations of length n.'''
    moves = get_possible_moves(board_)

    if n == 1:
        return moves
    
    else: 
        all_move_combos = []
        for move in moves:
            if move.find('#') != -1:
                all_move_combos.append(move)
                break
            board_.push_san(move)
            next_set = n_deep_nested(board_,n-1)
            for new_move in next_set:
                move_tuple = []
                move_tuple.append(move)
                move_tuple.append(new_move)
                all_move_combos.append(move_tuple)
            board_.pop()
            
    return all_move_combos

def tuple_cleaner(moves):
    '''Takes the move sequences from n_deep_nested and cleans them.'''
    branch = []
    while len(moves) == 2 and type(moves) == list:
        branch.append(moves[0])
        moves = moves[1]
    branch.append(moves)
    return branch

#######################################################################################
#Uses n_deep_nested and tuple_cleaner to produce all possible move strings of length n#
def moves_n_deep(board_, n):
    return [tuple_cleaner(string) for string in n_deep_nested(board_,n)]
#######################################################################################
#######################################################################################




####################################################################################
#####This function returns the point values of every possible move with depth n#####
def move_points_depth_n(board_,quantifier,n):
    '''Takes a board and returns all possible move combinations of length n.'''
    moves = get_possible_moves(board_)

        #No preference to Center Control
    #points = [how_many_points(move,board_) for move in moves]
        #Give Preference to Center Control
    points = [quantifier(move,board_) for move in moves]

    if n == 1:
        return points
    
    else: 
        all_move_points = []
        for i in range(len(moves)):
            if moves[i].find('#') != -1:
                all_move_points.append(points[i])
                break
            board_.push_san(moves[i])
            opp_move = move_points_depth_n(board_,quantifier, n-1)
            points_per_move = points[i] - max(opp_move)
            all_move_points.append(points_per_move)
            board_.pop()
            
    return all_move_points

#uses the above to make move
def comp_make_move(board_,moves_,n):
    possible_moves = get_possible_moves(board_)
    if len(moves_) < 8:    
        points = move_points_depth_n(board_,how_many_points_center, n)
    else:    
        points = move_points_depth_n(board_,how_many_points, n)
    max_indices = [i for i, val in enumerate(points) if val == max(points)]
    best_moves = [possible_moves[i] for i in max_indices]
    final_move = random.choice(best_moves)
    board_.push_san(final_move)
    moves_.append(final_move)
    if board_.is_game_over():
        print('Game Over!')
        print(board_.result())
        print(moves_)
    return board_
####################################################################################
####################################################################################