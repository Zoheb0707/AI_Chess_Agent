'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''



import BC_state_etc as BC
from copy import deepcopy
import random

def makeMove(currentState, currentRemark, timelimit):

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)
    curr_player = newState.whose_move
    gameBoard = newState.board
    all_moves = []

    for row in range(8):
        for col in range(8):
            piece = gameBoard[row][col]
            piece_side = BC.who(piece)
            if piece_side == curr_player and not piece == 0:
                # test if piece is immobilized
                immobile = isPieceImmobilized(row, col, gameBoard, curr_player)
                if not immobile:
                    if piece == BC.BLACK_PINCER or piece == BC.WHITE_PINCER:
                        p_moves = findPincerMoves(newState, (row, col))
                        for move in p_moves:       
                            all_moves.append(move)
                    elif piece == BC.BLACK_KING or piece == BC.WHITE_KING:
                        k_moves = findKingMoves(newState, (row, col))
                        for move in k_moves:
                            all_moves.append(move)
                    else:
                        q_moves = findQueenStyleMoves(newState, (row,col))
                        for move in q_moves:
                            all_moves.append(move)
                    

    #findPincerMoves(newState, (1,0))
    #findQueenStyleMoves(newState, (3, 2))
    #findQueenStyleMoves(newState, (3, 4))
    tup = random.choice(all_moves)
    #print("tuple: " + str(tup))
    move = tup[0]
    newState = tup[1]

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
        same_location = False
        for num in range(8):
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

            if num == 0 and (piece == BC.BLACK_LEAPER or piece == BC.WHITE_LEAPER):
                test_row = row
                test_col = col
                same_location = True

            if num == 1:
                same_location = False

            # test if this is a valid tile
            if test_row < 0 or test_row > 7:
                break
            if test_col < 0 or test_col > 7:
                break

            # if it is a blank tile
            if orig_board[test_row][test_col] == 0 or same_location:
                # do something
                #print("this is a blank tile!")

                # deep copy the lists of lists
                new_board = deepcopy(newState.board)

                # default non capturing move (moving into a blank space)
                if not same_location:
                    new_board[test_row][test_col] = piece
                    new_board[row][col] = 0

                cap_pieces = []

                ### capture enemy piece if possible
                if piece == BC.BLACK_COORDINATOR or piece == BC.WHITE_COORDINATOR:
                    # coordinator code
                    #print("i am a coordinator! please do coordinating things please! :)")
                    cap_pieces = coordCapMove(test_row, test_col, new_board, who)

                    #print("captured pieces: " + str(cap_pieces))
                # leaper may change target location
                elif piece == BC.BLACK_LEAPER or piece == BC.WHITE_LEAPER:
                    # leaper code
                    #print("i am a leaper! please do leapy things! :P")

                    # create new state to add to q moves potentially
                    leaper_state = BC.BC_state(new_board)
                    leap_tup = leaperCapMove(test_row, test_col, direction, who, curr_coord, leaper_state)
                    if not leap_tup == 0:
                        new_target = leap_tup[0]
                        cap_piece = leap_tup[1]
                        new_move = (curr_coord, new_target)
                        #print("leaper state: ")
                        #print(str(leaper_state))
                        #print("captured pieces: " + str(cap_piece))
                        q_moves.append((new_move, leaper_state, cap_piece))
                # imitator may change target location if imitating a leaper
                elif piece == BC.BLACK_IMITATOR or piece == BC.WHITE_IMITATOR:
                    # imitator code
                    print("i am an imitator! imitation is the sincerest form of flattery ;)")
                elif piece == BC.BLACK_WITHDRAWER or piece == BC.WHITE_WITHDRAWER:
                    # withdrawer code
                    #print("i am a withdrawer! i like to be anti-social T_T")
                    cap_pieces = withdrawerCapMove(row, col, direction, new_board, who)
        

                add_state = BC.BC_state(new_board)
                #print("added state:")
                #print(str(add_state))
                # target location is (test_row, test_col)
                move = (curr_coord, (test_row, test_col))

                # this is where a check to determine whether the new state is one where
                # the king is in check would occur; if the king is in check in the new
                # state, don't append the move and state to the list
                if not same_location:
                    q_moves.append((move, add_state, cap_pieces))
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
                piece_cap = pincerCapMove(test_row, test_col, direction, new_board, who)

                add_state = BC.BC_state(new_board)
                #print("added state:")
                #print(str(add_state))
                move = (curr_coord, (test_row, test_col))

                # this is where a check to determine whether the new state is one where
                # the king is in check would occur; if the king is in check in the new
                # state, don't append the move and state to the list
                p_moves.append((move, add_state, piece_cap))
                
            else:
                break
            # if its not blank, break out of loop

    return p_moves

def findKingMoves(state, curr_coord):
    who = state.whose_move
    newState = BC.BC_state(state.board)
    k_moves = []
    (king_row, king_col) = curr_coord
    piece = newState.board[king_row][king_col]
    test_row = king_row
    test_col = king_col
    test_piece = 99
    piece_cap = []

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        if direction == BC.NORTH:
            test_row = king_row - 1
        elif direction == BC.NE:
            test_row = king_row - 1
            test_col = king_col + 1
        elif direction == BC.EAST:
            test_col = king_col + 1
        elif direction == BC.SE:
            test_row = king_row + 1
            test_col = king_row + 1
        elif direction == BC.SOUTH:
            test_row = king_row + 1
        elif direction == BC.SW:
            test_row = king_row + 1
            test_col = king_col - 1
        elif direction == BC.WEST:
            test_col = king_col - 1
        elif direction == BC.NW:
            test_row = king_row - 1
            test_col = king_col - 1

        if test_row >= 0 and test_row <= 7 and test_col >=0 and test_col <= 7:
            test_piece = newState.board[test_row][test_col]

        test_piece_side = BC.who(test_piece)

        if not test_piece == 99:
            if test_piece == 0:
                piece_cap = []

                new_board = deepcopy(newState.board)
                new_board[test_row][test_col] = piece
                new_board[king_row][king_col] = 0

                move = (curr_coord, (test_row, test_col))

                add_state = BC.BC_state(new_board)

                k_moves.append((move, add_state, piece_cap))
            elif not test_piece_side == who:
                piece_cap = []
                piece_cap.append(test_piece)

                new_board = deepcopy(newState.board)
                new_board[test_row][test_col] = piece
                new_board[king_row][king_col] = 0

                move = (curr_coord, (test_row, test_col))

                add_state = BC.BC_state(new_board)

                k_moves.append((move, add_state, piece_cap))

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
    # default captured piece is empty list
    captured_pieces = []

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
        captured_pieces.append(enemy_piece)
        board[enemy_row][enemy_col] = 0

    return captured_pieces

def coordCapMove(dest_row, dest_col, board, cur_player):
    # intersection of king's rank and coordinator's file and coordinator's file
    # and king's rank are captured

    # pieces captured is initialized to an empty list
    captured_pieces = []

    (row_king, col_king) = findAllyKing(board, cur_player)

    # possible captured pieces
    cap_piece1 = board[row_king][dest_col]
    cap_piece2 = board[dest_row][col_king]

    #print("captured_piece1: " + str(cap_piece1))
    #print("captured_piece2: " + str(cap_piece2))

    # side of captured pieces
    piece1_side = BC.who(cap_piece1)
    piece2_side = BC.who(cap_piece2)
    

    # if captured piece 1 is an enemy, capture it!
    if not piece1_side == cur_player and not cap_piece1 == 0:
        captured_pieces.append(cap_piece1)
        board[row_king][dest_col] = 0

    # if captured piece 2 is an enemy, capture it!
    if not piece2_side == cur_player and not cap_piece2 == 0:
        captured_pieces.append(cap_piece2)
        board[dest_row][col_king] = 0
        
    return captured_pieces

    
                

def findAllyKing(test_board, who):
    # assign king to blank space as default
    king = 0

    # assign ally king
    if who == BC.WHITE:
        king = BC.WHITE_KING
    else:
        king = BC.BLACK_KING
    
    # find ally king location
    for test_row in range(8):
        for test_col in range(8):
            if test_board[test_row][test_col] == king:
                return (test_row, test_col)

    

def leaperCapMove(dest_row, dest_col, direction, cur_player, curr_coord, new_state):
    # can leap over any piece in diagonal line as long there is one tile of space
    # right after the enemy piece

    # test if this is a capture move or not
    enemy_row = dest_row
    enemy_col = dest_col
    empty_row = dest_row
    empty_col = dest_col
    # set ally piece and enemy piece to default invalid values
    empty_piece = 99
    enemy_piece = 99
    cap_test = False
    board = new_state.board
    piece = board[dest_row][dest_col]
    # default captured piece is empty list
    captured_pieces = []

    # capture test: piece one tile past is enemy piece and
    # piece one two tiles past is empty space
    if direction == BC.NORTH:
        enemy_row = dest_row - 1
        empty_row = dest_row - 2
        # empty space must be below top boundary of board
        if empty_row >= 0:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.NE:
        # increment NE
        enemy_row = dest_row - 1
        empty_row = dest_row - 2
        enemy_col = dest_col + 1
        empty_col = dest_col + 2
        if empty_col <= 7 and empty_row >= 0:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.EAST:
        # increment east
        enemy_col = dest_col + 1
        empty_col = dest_col + 2
        if empty_col <= 7:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SE:
        # increment SE
        enemy_row = dest_row + 1
        empty_row = dest_row + 2
        enemy_col = dest_col + 1
        empty_col = dest_col + 2
        if empty_col <= 7 and empty_row <= 7:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SOUTH:
        # increment south
        enemy_row = dest_row + 1
        empty_row = dest_row + 2
        if empty_row <= 7:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SW:
        # increment SW
        enemy_row = dest_row + 1
        empty_row = dest_row + 2
        enemy_col = dest_col - 1
        empty_col = dest_col - 2
        if empty_col >= 0 and empty_row <= 7:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.WEST:
        # increment west
        enemy_col = dest_col - 1
        empty_col = dest_col - 2
        if empty_col >= 0:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.NW:
        # increment NW
        enemy_row = dest_row - 1
        empty_row = dest_row - 2
        enemy_col = dest_col - 1
        empty_col = dest_col - 2
        if empty_col >= 0 and empty_row >= 0:
            empty_piece = board[empty_row][empty_col]
            enemy_piece = board[enemy_row][enemy_col]

    # empty space and enemy piece must be valid
    if not empty_piece == 99 and not enemy_piece == 99:
        enemy_side = BC.who(enemy_piece)
        # if other space is empty, and the
        # captured piece is an enemy
        if empty_piece == 0 and not enemy_side == cur_player and not enemy_piece == 0:
            cap_test = True

    if cap_test:
        new_board = new_state.board
        #print("piece: " + str(piece))
        new_board[empty_row][empty_col] = piece
        new_board[dest_row][dest_col] = 0
        captured_pieces.append(enemy_piece)
        new_board[enemy_row][enemy_col] = 0
        # return the new target location and captured piece (board has been modified in place)
        return ((empty_row, empty_col), captured_pieces)
    else:
        return 0

    

# one of the hardest to code
def imitatorCapMove(dest_row, dest_col, direction, board, cur_player):
    print("imitator doesn't know how to capture")
    # tbh i have no idea how to code this one i'll figure it out later

def withdrawerCapMove(orig_row, orig_col, direction, board, cur_player):
    # if enemy was directly adjacent to withdrawer in the opposite direction of
    # withdrawer's movement, the enemy is captured

    # board will be modified in place (no need for a deep copy of the state)

    enemy_row = orig_row
    enemy_col = orig_col
    enemy_piece = 0
    cap_piece = []
    
    if direction == BC.NORTH:
        # test one tile south of original location to see if it's an enemy
        enemy_row = orig_row + 1
        if enemy_row <= 7:
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.NE:
        # test SW
        enemy_row = orig_row + 1
        enemy_col = orig_col - 1
        if enemy_row <= 7 and enemy_col >= 0:
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.EAST:
        # test W
        enemy_col = orig_col - 1
        if enemy_col >= 0:
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SE:
        # test NW
        enemy_row = orig_row - 1
        enemy_col = orig_col - 1
        if enemy_row >= 0 and enemy_col >= 0:
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SOUTH:
        # test N
        enemy_row = orig_row - 1
        if enemy_row >= 0:
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.SW:
        # test NE
        enemy_row = orig_row - 1
        enemy_col = orig_col + 1
        if enemy_row >= 0 and enemy_col <= 7:
            enemy_piece = board[enemy_row][enemy_col]
    # below part not right
    elif direction == BC.WEST:
        # test E
        enemy_col = orig_col + 1
        if enemy_col <= 7:
            enemy_piece = board[enemy_row][enemy_col]
    elif direction == BC.NW:
        # test SE
        enemy_row = orig_row + 1
        enemy_col = orig_col + 1
        if enemy_row <= 7 and enemy_col <= 7:
            enemy_piece = board[enemy_row][enemy_col]

    enemy_side = BC.who(enemy_piece)

    if not enemy_side == cur_player and not enemy_piece == 0:
        cap_piece.append(enemy_piece)
        board[enemy_row][enemy_col] = 0

    return cap_piece
        
def isPieceImmobilized(piece_row, piece_col, board, curr_player):
    freezer = 0
    test_row = piece_row
    test_col = piece_col

    if curr_player == BC.WHITE:
        freezer = BC.BLACK_FREEZER
    else:
        freezer = BC.WHITE_FREEZER

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        if direction == BC.NORTH:
            test_row = piece_row - 1
        elif direction == BC.NE:
            test_row = piece_row - 1
            test_col = piece_col + 1
        elif direction == BC.EAST:
            test_col = piece_col + 1
        elif direction == BC.SE:
            test_row = piece_row + 1
            test_col = piece_row + 1
        elif direction == BC.SOUTH:
            test_row = piece_row + 1
        elif direction == BC.SW:
            test_row = piece_row + 1
            test_col = piece_col - 1
        elif direction == BC.WEST:
            test_col = piece_col - 1
        elif direction == BC.NW:
            test_row = piece_row - 1
            test_col = piece_col - 1

        if test_row >= 0 and test_row <= 7 and test_col >=0 and test_col <= 7:
            test_piece = board[test_row][test_col]

        if test_piece == freezer:
            return True

    return False
    
    

# have not implemented test for determining whether the king is in check or not
#def isKingInCheck(state):

# add possible pieces that can be killed in a given move to the tuple returned
def canMove(curr_coord, final_coord, state):
    move_test = False
    (row, col) = curr_coord
    piece = state.board[row][col]

    moves = []
    if piece == BC.BLACK_PINCER or piece == BC.WHITE_PINCER:
        moves = findPincerMoves(state, curr_coord)
    elif piece == BC.BLACK_KING or piece == BC.WHITE_KING:
        moves = findKingMoves(state, curr_coord)
    else:
        moves = findQueenStyleMoves(state, curr_coord)

    for tup in moves:
        move = tup[0]
        if final_coord == move:
            move_test = True

    return move_test



