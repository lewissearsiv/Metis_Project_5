import chess 
import random
from chess_workhorse_tools import *

def points_dynamic_depth(board_,move_, depth):
    '''Given a board and a single move we create a minimax optimization pattern that goes to a desired depth.
    Note that once the depth approaches 4 this process becomes very slow.'''

    #Initialize the points    
    points = how_many_points(move_,board_)*(-1)**(2-depth)

    board_.push_san(move_)
    new_moves = get_possible_moves(board_)
    return [points + points_dynamic_depth(board_, move, depth-1) for move in new_moves]




#stolen sample python3 minimax

import math 
  
def minimax (curDepth, nodeIndex, maxTurn, scores, targetDepth): 
  
    # base case : targetDepth reached 
    if (curDepth == targetDepth):  
        return scores[nodeIndex] 
      
    if (maxTurn): 
        return max(minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth), minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth)) 
      
    else: 
        return min(minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth), minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth))
