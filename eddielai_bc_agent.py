'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''



import BC_state_etc as BC
from copy import deepcopy

def makeMove(currentState, currentRemark, timelimit):

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    findPincerMoves(newState, (6, 0))

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

def nickname():
    return "Newman"

def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."

def prepare(player2Nickname):
    pass

# finding all possible moves for a specific board state

# each method returns a list of tuples; (move, new board state)
# format for moves is as follows: (original coordinates of piece,
# new coordinates of piece)

# whose_move: 1 is white, 0 is black


def findLeaperMoves(state, curr_coord):
    who = state.whose_move
    l_moves = []
    #gameBoard = state.board

    #print("board state: ")
    #print(str(state))

    return l_moves

# may change this function later
def findQueenStyleMoves(state, curr_coord):
    # deep copy the current state into a new state
    orig_board = state.board
    newState = BC.BC_state(orig_board)
    who = state.whose_move
    
    q_moves = []
    (row, col) = curr_coord
    (test_row, test_col) = curr_coord
    piece = orig_board[row][col]

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        test_row = row
        test_col = col
        for num in range(7):
            if direction == BC.NORTH:
                # increment north one tile
                test_row = test_row - 1
                #print("north")
            elif direction == BC.NE:
                # increment northeast one tile
                test_row = test_row - 1
                test_col += 1
                #print("ne")
            elif direction == BC.EAST:
                # increment east one tile
                test_col += 1
                #print("east")
            elif direction == BC.SE:
                # increment southeast one tile
                test_row += 1
                test_col += 1
            elif direction == BC.SOUTH:
                # increment south one tile
                test_row += 1
                #print("south")
            elif direction == BC.SW:
                # increment southwest one tile
                test_row += 1
                test_col = test_col - 1
                #print("sw")
            elif direction == BC.WEST:
                # increment west one tile
                test_col = test_col - 1
                #print("west")
            elif direction == BC.NW:
                # increment nw one tile
                test_row = test_row - 1
                test_col = test_col - 1

            # test if this is a valid tile
            if test_row < 0 or test_row > 7:
                break
            if test_col < 0 or test_col > 7:
                break

            # if it is a blank tile
            if orig_board[test_row][test_col] == 0:
                # do something
                #print("this is a blank tile!")

                # deep copy the lists of lists
                new_board = deepcopy(newState.board)
                new_board[test_row][test_col] = piece
                new_board[row][col] = 0

                ### capture enemy piece if possible
                if piece == BC.BLACK_COORDINATOR or piece == BC.WHITE_COORDINATOR:
                    # coordinator code
                    print("i am a coordinator! please do coordinating things please! :)")
                # leaper may change target location
                elif piece == BC.BLACK_LEAPER or piece == BC.WHITE_LEAPER:
                    # leaper code
                    print("i am a leaper! please do leapy things! :P")
                # imitator may change target location if imitating a leaper
                elif piece == BC.BLACK_IMITATOR or piece == BC.WHITE_IMITATOR:
                    # imitator code
                    print("i am an imitator! imitation is the sincerest form of flattery ;)")
                elif piece == BC.BLACK_WITHDRAWER or piece == BC.WHITE_WITHDRAWER:
                    # withdrawer code
                    print("i am a withdrawer! i like to be anti-social T_T")
        

                add_state = BC.BC_state(new_board)
                #print("added state:")
                #print(str(add_state))

                # target location is (test_row, test_col)
                move = (curr_coord, (test_row, test_col))

                # this is where a check to determine whether the new state is one where
                # the king is in check would occur; if the king is in check in the new
                # state, don't append the move and state to the list
                q_moves.append((move, add_state))
            else:
                break
    
    return q_moves

def findPincerMoves(state, curr_coord):
    newState = BC.BC_state(state.board)
    who = state.whose_move
    #print("who am i: " + str(who))
    p_moves = []
    orig_board = state.board
    (row, col) = curr_coord
    (test_row, test_col) = curr_coord
    piece = orig_board[row][col]

    move_dir = [BC.NORTH, BC.EAST, BC.SOUTH, BC.WEST]

    for direction in move_dir:
        test_row = row
        test_col = col
        for num in range(7):
            if direction == BC.NORTH:
                # increment north one tile
                test_row = test_row - 1
                #print("north")
            elif direction == BC.EAST:
                # increment east one tile
                test_col += 1
                #print("east")
            elif direction == BC.SOUTH:
                # increment south one tile
                test_row += 1
                #print("south")
            elif direction == BC.WEST:
                # increment west one tile
                test_col = test_col - 1
                #print("west")

            # test if this is a valid tile
            if test_row < 0 or test_row > 7:
                break
            if test_col < 0 or test_col > 7:
                break

            
            # if it is blank, add move and new state to list of tuples
            if orig_board[test_row][test_col] == 0:

                # deep copy the lists of lists
                new_board = deepcopy(newState.board)
                new_board[test_row][test_col] = piece
                new_board[row][col] = 0

                # capture enemy piece if possible
                pincerCapMove(test_row, test_col, direction, new_board, who)

                add_state = BC.BC_state(new_board)
                #print("added state:")
                #print(str(add_state))
                move = (curr_coord, (test_row, test_col))

                # this is where a check to determine whether the new state is one where
                # the king is in check would occur; if the king is in check in the new
                # state, don't append the move and state to the list
                p_moves.append((move, add_state))
                
            else:
                break
            # if its not blank, break out of loop

    return p_moves

def findKingMoves(state, curr_coord):
    who = state.whose_move
    k_moves = []

    return k_moves

# this function takes a given board and captures an enemy piece via the Pincer
# attack if it is possible to according to Baroque Chess rules
def pincerCapMove(dest_row, dest_col, direction, board, cur_player):
    # test if this is a capture move or not
    enemy_row = dest_row
    enemy_col = dest_col
    ally_row = dest_row
    ally_col = dest_col
    # set ally piece and enemy piece to default blank spaces
    ally_piece = 0
    enemy_piece = 0
    cap_test = False

    # capture test: piece one tile past is enemy piece and
    # piece one two tiles past is friendly piece
    if direction == BC.NORTH:
        enemy_row = dest_row - 1
        ally_row = dest_row - 2
        # ally must be below top boundary of board
        if ally_row >= 0:
            ally_piece = board[ally_row][ally_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.EAST:
        # increment east
        enemy_col = dest_col + 1
        ally_col = dest_col + 2
        if ally_col <= 7:
            ally_piece = board[ally_row][ally_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SOUTH:
        # increment south
        enemy_row = dest_row + 1
        ally_row = dest_row + 2
        if ally_row <= 7:
            ally_piece = board[ally_row][ally_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.WEST:
        # increment west
        enemy_col = dest_col - 1
        ally_col = dest_col - 2
        if ally_col >= 0:
            ally_piece = board[ally_row][ally_col]
            enemy_piece = board[enemy_row][enemy_col]

    # if friend and enemy are not blank
    if not ally_piece == 0 and not enemy_piece == 0:
        ally_side = BC.who(ally_piece)
        enemy_side = BC.who(enemy_piece)
        # if other pincer is friendly, and the
        # captured piece is an enemy
        if ally_side == cur_player and not enemy_side == cur_player:
            cap_test = True

    #print("value of enemy: " + str(enemy_piece))
    #print("value of ally: " + str(ally_piece))
    #print("value of cap_test: " + str(cap_test))

    if cap_test:
        # capture enemy piece
        board[enemy_row][enemy_col] = 0

def coordCapMove():
    print("coordinator doesn't know how to capture")
    # intersection of king's rank and coordinator's file and coordinator's file
    # and king's rank are captured

def leaperCapMove():
    print("leaper doesn't know how to capture")
    # can leap over any piece in diagonal line as long there is one tile of space
    # right after the enemy piece 

# one of the hardest to code
def imitatorCapMove():
    print("imitator doesn't know how to capture")
    # tbh i have no idea how to code this one i'll figure it out later

def withdrawerCapMove():
    print("withdrawer doesn't know how to capture")
    # if enemy was directly adjacent to withdrawer in the opposite direction of
    # withdrawer's movement, the enemy is captured
    

# have not implemented test for determining whether the king is in check or not
#def isKingInCheck(state):
    




