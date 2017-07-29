#Minimax vs. minimax
#Alpha-beta vs. alpha-beta
#Minimax vs. alpha-beta (minimax goes first)
#Alpha-beta vs. minimax (alpha-beta goes first)

#offensive(1st) vs Defensive
#defensive(1st) vs offensive
#Offensive vs offensive
#Defensive vs Defensive

import numpy as np
import copy
import time
import os
import sys

board_width = 8
board_height = 8


def print_board(black, white):
    global board_width
    global board_height

    board = [['_' for x in range(board_height)] for x in range(board_width)] 
    
    for i in black:
        board[black[i][0]][black[i][1]] = 'X'
    for i in white:
        board[white[i][0]][white[i][1]] = 'O'

    for l in board:
        print(l)


# return True if game ends
def terminal_black_test(black, white):
    if white == {}:
        # print('Empty! Black Wins!')
        # print_board(black, white)
        return True
    global board_height
    for b in black:
        if black[b][0] == board_height-1:
            # print('Reach Base! Black Wins!')
            # print_board(black, white)
            return True
    return False

def terminal_white_test(white, black):
    if black == {}:
        # print('Empty! White Wins!')
        # print_board(black, white)
        return True
    for w in white:
        if white[w][0] == 0:
            # print('Reach Base! White Wins!')
            # print_board(black, white)
            return True
    return False


def cutoff_test(black, white, depth):
    if depth >= 3:
        return True
    return False



def black_score(black):
    global board_height

    black_num_score = len(black)
    black_dist_score = max([black[i][0] for i in black])
    return black_num_score + black_dist_score

def white_score(white):
    global board_height

    white_num_score = len(white)
    white_dist_score = board_height-1 - min([white[i][0] for i in white])
    return white_num_score + white_dist_score

# going down
def offensive_heuristic_black(black, white):
    # print('offensive_heuristic_black')

    # for i in black:
    #     pos = black[i]
    #     self_dist_score += 4*pos[0]

    # for i in white:
    #     pos = white[i]
    #     opponent_dist_score += 4*(board_height-1-pos[0])

    self_score = black_score(black)
    opponent_score = white_score(white)

    heuristic = 0.8*self_score - 0.2*opponent_score
    return heuristic

# going down
def defensive_heuristic_black(black, white):
    # global board_height
    # self_dist_score = 0
    # opponent_dist_score = 0

    # for i in black:
    #     pos = black[i]
    #     self_dist_score += 4*pos[0]
    # self_num_score = len(black)

    # for i in white:
    #     pos = white[i]
    #     opponent_dist_score += 4*(board_height-1-pos[0])
    # opponent_num_score = len(white)
    
    self_score = black_score(black)
    opponent_score = white_score(white)

    heuristic = 0.2*self_score - 0.8*opponent_score
    return heuristic


# going up
def offensive_heuristic_white(white, black):

    # for i in white:
    #     pos = white[i]
    #     self_dist_score += 4*(board_height-1-pos[0])

    # for i in black:
    #     pos = black[i]
    #     opponent_dist_score += 4*pos[0]

    self_score = white_score(white)
    opponent_score = black_score(black)

    heuristic = 2*self_score - 0.3*opponent_score
    return heuristic

# going up
def defensive_heuristic_white(white, black):
    # print('defensive_heuristic_white')
    # global board_height
    # self_dist_score = 0
    # opponent_dist_score = 0

    # for i in white:
    #     pos = white[i]
    #     self_dist_score += 4*(board_height-1-pos[0])
    # self_num_score = len(white)

    # for i in black:
    #     pos = black[i]
    #     opponent_dist_score += 4*pos[0]
    # opponent_num_score = len(black)

    self_score = white_score(white)
    opponent_score = black_score(black)

    heuristic = 0.3*self_score - 2*opponent_score
    return heuristic




# return all possible actions for black going down
def black_actions(black, white):
    actions = []
    global board_width
    global board_height

    for i in black:
        pos = black[i]
        # no one is in front
        if pos[0]+1 < board_height or ((pos[0]+1, pos[1]) not in white.values()) or ((pos[0]+1, pos[1]) not in black.values()):
            actions.append( (i, (pos[0]+1, pos[1])) )
        # down right possible
        if pos[0]+1 < board_height or pos[1]+1 < board_width or ((pos[0]+1, pos[1]+1) not in black.values()):
            actions.append( (i, (pos[0]+1, pos[1]+1)) )
        # down left possible
        if pos[0]+1 < board_height or pos[1]-1 >= 0 or ((pos[0]+1, pos[1]-1) not in black.values()):
            actions.append( (i, (pos[0]+1, pos[1]-1)) )          

    # print('black_actions')
    # for a in actions:
    #     print(a)
    # print()

    return actions

# return all possible actions for white going up
def white_actions(white, black):
    actions = []
    global board_width
    global board_height

    for i in white:
        pos = white[i]
        # black is not in front
        if pos[0]-1 >= 0 or ((pos[0]-1, pos[1]) not in black.values()) or ((pos[0]-1, pos[1]) not in white.values()):
            actions.append( (i, (pos[0]-1, pos[1])) )
        # up right possible
        if pos[0]-1 >= 0 or pos[1]+1 < board_width or ((pos[0]-1, pos[1]+1) not in white.values()):
            actions.append( (i, (pos[0]-1, pos[1]+1)) )
        # up left possible
        if pos[0]-1 >= 0 or pos[1]-1 >= 0 or ((pos[0]-1, pos[1]-1) not in white.values()):
            actions.append( (i, (pos[0]-1, pos[1]-1)) )

    # print('white_actions')
    # for a in actions:
    #     print(a)
    # print()

    return actions






#################################### alpha beta white  decision ############################################

# white's turn
# returns a utility value
def alphabeta_max_value_white(white, black, depth, alpha, beta):
    if cutoff_test(black, white, depth):
        # print('max_value_white')
        return defensive_heuristic_white(white, black)
    # print('max_value_black', depth)

    v = -sys.maxsize - 1
    for a in white_actions(white, black):
        # do action on copies
        tmp_white = dict(white)
        tmp_white[a[0]] = a[1]
        tmp_black = dict((k, v) for k, v in black.items() if v != a[1])
        
        # print('white action:', a, depth+!)
        # print_board(tmp_black, tmp_white)
        # print()

        # if white wins
        if terminal_white_test(tmp_white, tmp_black):
            return sys.maxsize

        v = max(v, alphabeta_min_value_white(tmp_white, tmp_black, depth+1, alpha, beta))

        if v >= beta:
            return v
        alpha = max(alpha, v)

    return v

# black's turn
# returns a utility value
def alphabeta_min_value_white(white, black, depth, alpha, beta):
    if cutoff_test(black, white, depth):
        # print('min_value_white')
        heuristic = defensive_heuristic_white(white, black)
        return heuristic
    # print('min_value_black', depth)
    

    v = sys.maxsize
    for a in black_actions(black, white):
        # do action on copies
        tmp_black = dict(black)
        tmp_black[a[0]] = a[1]
        tmp_white = dict((k, v) for k, v in white.items() if v != a[1])

        # print('black action:', a, depth+1)
        # print_board(tmp_black, tmp_white)
        # print()

        # if black wins
        if terminal_black_test(tmp_black, tmp_white):
            return -sys.maxsize-1

        v = min(v, alphabeta_max_value_white(tmp_white, tmp_black, depth+1, alpha, beta))

        if v <= alpha:
            return v
        beta = min(beta, v)
                
    return v
            
# white's turn
# returns an action for white
def alphabeta_minimax_white_decision(white, black):
    v = -sys.maxsize - 1
    action = (-1,(-1,-1))
    print('minimax_white_decision')

    # who plays first
    for a in white_actions(white, black):
        # print('white action:', a, 1)
        # print()

        # do action on copies
        tmp_white = dict(white)
        tmp_white[a[0]] = a[1]
        tmp_black = dict((k, v) for k, v in black.items() if v != a[1])

        # print_board(tmp_black, tmp_white)
        # print()

        # resursion with copies
        max_value = max(v, alphabeta_min_value_white(tmp_white, tmp_black, 1, -sys.maxsize - 1, sys.maxsize))

        # if white wins
        if terminal_white_test(tmp_white, tmp_black):
            return a

        if max_value > v:
            action = a
            v = max_value
            # print('max_value:', max_value, 'white action:', action)
            # print()
    
    if max_value == -sys.maxsize - 1:
        return a

    return action


#################################### alpha beta black  decision ############################################
  
# black's turn  
# returns a utility value
def alphabeta_max_value_black(black, white, depth, alpha, beta):
    if cutoff_test(black, white, depth):
        return offensive_heuristic_black(black, white)    
    # print('max_value_black', depth)

    v = -sys.maxsize - 1
    for a in black_actions(black, white):
        # do action on copies
        tmp_black = dict(black)
        tmp_black[a[0]] = a[1]
        tmp_white = dict((k, v) for k, v in white.items() if v != a[1])
        
        # print('black action:', a)
        # print_board(tmp_black, tmp_white)
        # print()

        # if black wins
        if terminal_black_test(tmp_black, tmp_white):
            return sys.maxsize

        v = max(v, alphabeta_min_value_black(tmp_black, tmp_white, depth+1, alpha, beta))

        if v >= beta:
            return v
        alpha = max(alpha, v)

    return v


# white's turn
# returns a utility value
def alphabeta_min_value_black(black, white, depth, alpha, beta):
    if cutoff_test(black, white, depth):
        heuristic = offensive_heuristic_black(black, white)
        # print(heuristic)
        # print()
        return heuristic
    # print('min_value_black', depth)

    v = sys.maxsize
    for a in white_actions(white, black):
        # do action on copies
        tmp_white = dict(white)
        tmp_white[a[0]] = a[1]
        tmp_black = dict((k, v) for k, v in black.items() if v != a[1])

        # print('white action:', a)
        # print_board(tmp_black, tmp_white)
        # print()

        # if white wins
        if terminal_white_test(tmp_white, tmp_black):
            return -sys.maxsize-1

        v = min(v, alphabeta_max_value_black(tmp_black, tmp_white, depth+1, alpha, beta))

        if v <= alpha:
            return v
        beta = min(beta, v)

    return v
            

# black's turn
# returns an action for black
def alphabeta_minimax_black_decision(black, white):
    # smallest int value
    v = -sys.maxsize - 1
    action = (-1,(-1,-1))
    print('minimax_black_decision')

    # who plays first
    for a in black_actions(black, white):
        # print('black action:', a)
        # print()

        # do action on copies
        tmp_black = dict(black)
        tmp_black[a[0]] = a[1]
        tmp_white = dict((k, v) for k, v in white.items() if v != a[1])

        # print_board(tmp_black, tmp_white)
        # print()

        # resursion with copies
        max_value = max(v, alphabeta_min_value_black(tmp_black, tmp_white, 1, -sys.maxsize - 1, sys.maxsize))

        # if white wins
        if terminal_black_test(tmp_black, tmp_white):
            return a

        if max_value > v:
            action = a
            v = max_value
            # print('max_value:', max_value, 'action:', action)
            # print()

    if max_value == -sys.maxsize - 1:
        return a

    return action


################################################################################








#################################### white  decision ############################################

# white's turn
# returns a utility value
def max_value_white(white, black, depth):
    if cutoff_test(black, white, depth):
        # print('max_value_white')
        return defensive_heuristic_white(white, black)
    # print('max_value_black', depth)

    v = -sys.maxsize - 1
    for a in white_actions(white, black):
        # do action on copies
        tmp_white = dict(white)
        tmp_white[a[0]] = a[1]
        tmp_black = dict((k, v) for k, v in black.items() if v != a[1])
        
        # print('white action:', a, depth+!)
        # print_board(tmp_black, tmp_white)
        # print()

        # if white wins
        if terminal_white_test(tmp_white, tmp_black):
            return sys.maxsize

        v = max(v, min_value_white(tmp_white, tmp_black, depth+1))
    return v

# black's turn
# returns a utility value
def min_value_white(white, black, depth):
    if cutoff_test(black, white, depth):
        # print('min_value_white')
        heuristic = defensive_heuristic_white(white, black)
        return heuristic
    # print('min_value_black', depth)
    

    v = sys.maxsize
    for a in black_actions(black, white):
        # do action on copies
        tmp_black = dict(black)
        tmp_black[a[0]] = a[1]
        tmp_white = dict((k, v) for k, v in white.items() if v != a[1])

        # print('black action:', a, depth+1)
        # print_board(tmp_black, tmp_white)
        # print()

        # if black wins
        if terminal_black_test(tmp_black, tmp_white):
            return -sys.maxsize-1

        v = min(v, max_value_white(tmp_white, tmp_black, depth+1))
    return v
            
# white's turn
# returns an action for white
def minimax_white_decision(white, black):
    v = -sys.maxsize - 1
    action = (-1,(-1,-1))
    print('minimax_white_decision')

    # who plays first
    for a in white_actions(white, black):
        # print('white action:', a, 1)
        # print()

        # do action on copies
        tmp_white = dict(white)
        tmp_white[a[0]] = a[1]
        tmp_black = dict((k, v) for k, v in black.items() if v != a[1])

        # print_board(tmp_black, tmp_white)
        # print()

        # resursion with copies
        max_value = max(v, min_value_white(tmp_white, tmp_black, 1))

        # if white wins
        if terminal_white_test(tmp_white, tmp_black):
            return a
        
        # if a == (15, (6,7)):
        #     print('max_value:', max_value, 'white action:', a)
        #     print()

        if max_value > v:
            action = a
            v = max_value
            # print('max_value:', max_value, 'white action:', action)
            # print()
    
    if max_value == -sys.maxsize - 1:
        return a

    return action


#################################### black  decision ############################################
  
# black's turn  
# returns a utility value
def max_value_black(black, white, depth):
    if cutoff_test(black, white, depth):
        return offensive_heuristic_black(black, white)    
    # print('max_value_black', depth)

    v = -sys.maxsize - 1
    for a in black_actions(black, white):
        # do action on copies
        tmp_black = dict(black)
        tmp_black[a[0]] = a[1]
        tmp_white = dict((k, v) for k, v in white.items() if v != a[1])
        
        # print('black action:', a)
        # print_board(tmp_black, tmp_white)
        # print()

        # if black wins
        if terminal_black_test(tmp_black, tmp_white):
            return sys.maxsize


        v = max(v, min_value_black(tmp_black, tmp_white, depth+1))
    return v


# white's turn
# returns a utility value
def min_value_black(black, white, depth):
    if cutoff_test(black, white, depth):
        heuristic = offensive_heuristic_black(black, white)
        # print(heuristic)
        # print()
        return heuristic
    # print('min_value_black', depth)

    v = sys.maxsize
    for a in white_actions(white, black):
        # do action on copies
        tmp_white = dict(white)
        tmp_white[a[0]] = a[1]
        tmp_black = dict((k, v) for k, v in black.items() if v != a[1])

        # print('white action:', a)
        # print_board(tmp_black, tmp_white)
        # print()

        # if white wins
        if terminal_white_test(tmp_white, tmp_black):
            return -sys.maxsize-1

        v = min(v, max_value_black(tmp_black, tmp_white, depth+1))
    return v
            

# black's turn
# returns an action for black
def minimax_black_decision(black, white):
    # smallest int value
    v = -sys.maxsize - 1
    action = (-1,(-1,-1))
    print('minimax_black_decision')

    # who plays first
    for a in black_actions(black, white):
        # print('black action:', a)
        # print()

        # do action on copies
        tmp_black = dict(black)
        tmp_black[a[0]] = a[1]
        tmp_white = dict((k, v) for k, v in white.items() if v != a[1])

        # print_board(tmp_black, tmp_white)
        # print()

        # resursion with copies
        max_value = max(v, min_value_black(tmp_black, tmp_white, 1))

        # if white wins
        if terminal_black_test(tmp_black, tmp_white):
            return a

        if max_value > v:
            action = a
            v = max_value
            # print('max_value:', max_value, 'action:', action)
            # print()

    if max_value == -sys.maxsize - 1:
        return a

    return action


################################################################################







def main():
    # black goes first, goes down
    # white goes second, goes up
    
    # initialize black/white
    i = 0
    black = {}
    for y in range(0,2):
        for x in range(0,board_width):
            black[i] = (y, x)
            i+=1
    i = 0
    white = {}
    for y in range(board_height-2,board_height):
        for x in range(0,board_width):
            white[i] = (y, x)
            i+=1

    # print('black')
    # for i in black:
    #     print(i)
    # print('white')
    # for i in white:
    #     print(i)

    print_board(black, white)
    print()

    actions = []
    game_rounds = 0
    while True:
        print('game_rounds', game_rounds)        

        # white[0] = (white[0][0]-1, white[0][1] )
        # if terminal_white_test(black, white):
        #     break

        if game_rounds%2 == 1:
            #action = minimax_black_decision(black, white)
            action = alphabeta_minimax_black_decision(black, white)

            actions.append((game_rounds, 'black', action))
            # do the action
            black[action[0]] = action[1]
            white = dict((k, v) for k, v in white.items() if v != action[1])
            
            print('black final action:', action)
            print_board(black, white)
            print()

            if terminal_black_test(black, white):
                print('black wins!')
                print_board(black, white)
                break
        
        else:
            #action = minimax_white_decision(white, black)
            action = alphabeta_minimax_white_decision(white, black)

            actions.append((game_rounds, 'white', action))
            # do the action
            white[action[0]] = action[1]
            black = dict((k, v) for k, v in black.items() if v != action[1])

            print('white final action:', action)
            print_board(black, white)
            print()

            if terminal_white_test(white, black):
                print('white wins!')
                print_board(black, white)
                break

        game_rounds += 1

        
        # test first step
        # if game_rounds == 1:
        #     print('game_rounds', game_rounds)
        #     break






if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
