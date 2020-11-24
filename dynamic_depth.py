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

def n_moves_points(moves_, board_):

    #Initialize points
    points = 0
    
    for i, move in enumerate(moves_):
        #This gives the min/max sign
        min_or_max = (-1)**i
        points += (how_many_points(move, board_) * min_or_max)
        board_.push_san(move)

    #Reset the board
    i = 0 
    while i < len(moves_):
        board_.pop()
        i += 1

    return points

def n_optimized_move(board_,moves_,n):
    possible_moves = get_possible_moves(board_)
    move_combos = n_deep_nested(board_, n)
    cleaned_branches = [tuple_cleaner(move) for move in move_combos]
    points_per_branch = [n_moves_points(branch, board_) for branch in cleaned_branches]


#Put something here to make the points work.

    
    final_move = random.choice(best_moves)
    board_.push_san(final_move[0])
    moves_.append(final_move[0])
    if board_.is_game_over():
        print('Game Over!')
        print(board_.result())
        print(moves_)
    return board_



