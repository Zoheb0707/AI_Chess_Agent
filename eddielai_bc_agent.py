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
    who = state.whose_move
    q_moves = []
    
    return q_moves

def findPincerMoves(state, curr_coord):
    newState = BC.BC_state(state.board)
    who = state.whose_move
    print("who am i: " + str(who))
    p_moves = []
    orig_board = state.board
    (row, col) = curr_coord
    (test_row, test_col) = curr_coord
    piece = orig_board[row][col]

    move_dir = [BC.NORTH, BC.EAST, BC.SOUTH, BC.WEST]

    for direction in move_dir:
        test_row = row
        test_col = col
        for num in range(8):
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

                # test if this is a capture move or not
                enemy_row = test_row
                enemy_col = test_col
                ally_row = test_row
                ally_col = test_col
                # set ally piece and enemy piece to default blank spaces
                ally_piece = 0
                enemy_piece = 0
                cap_test = False
                # capture test: piece one tile past is enemy piece and
                # piece one two tiles past is friendly piece
                if direction == BC.NORTH:
                    enemy_row = test_row - 1
                    ally_row = test_row - 2
                    # ally must be below top boundary of board
                    if ally_row >= 0:
                        ally_piece = orig_board[ally_row][ally_col]
                        enemy_piece = orig_board[enemy_row][enemy_col]
                elif direction == BC.EAST:
                    # increment east
                    enemy_col = test_col + 1
                    ally_col = test_col + 2
                    if ally_col <= 7:
                        ally_piece = orig_board[ally_row][ally_col]
                        enemy_piece = orig_board[enemy_row][enemy_col]
                elif direction == BC.SOUTH:
                    # increment south
                    enemy_row = test_row + 1
                    ally_row = test_row + 2
                    if ally_col <= 7:
                        ally_piece = orig_board[ally_row][ally_col]
                        enemy_piece = orig_board[enemy_row][enemy_col]
                elif direction == BC.WEST:
                    # increment west
                    enemy_col = test_col - 1
                    ally_col = test_col - 2
                    if ally_col >= 0:
                        ally_piece = orig_board[ally_row][ally_col]
                        enemy_piece = orig_board[enemy_row][enemy_col]

                # if friend and enemy are not blank
                if not ally_piece == 0 and not enemy_piece == 0:
                    ally_side = BC.who(ally_piece)
                    enemy_side = BC.who(enemy_piece)
                    # if other pincer is friendly, and the
                    # captured piece is an enemy
                    if ally_side == who and not enemy_side == who:
                        cap_test = True

                # deep copy the lists of lists
                new_board = deepcopy(newState.board)
                new_board[test_row][test_col] = piece
                new_board[row][col] = 0
                #print("value of enemy: " + str(enemy_piece))
                #print("value of ally: " + str(ally_piece))
                #print("value of cap_test: " + str(cap_test))

                if cap_test:
                    # capture enemy piece
                    new_board[enemy_row][enemy_col] = 0

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

# have not implemented test for determining whether the king is in check or not
#def isKingInCheck(state):
    




