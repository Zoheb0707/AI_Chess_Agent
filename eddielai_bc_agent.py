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
    curr_player = currentState.whose_move
    gameBoard = newState.board
    all_moves = []
    print("current player: " + str(curr_player))

    generatedMoves = generateNewMoves(currentState, curr_player)
    
    # generatedMoves contains tuples that are in the form of:
    # (move, state, pieces_captured)

    # to extract the things needed to be returned at the end of this makeMove function,
    # you take the first two elements of each tuple in generatedMoves

    # i.e.
    '''
    for move_tup in generatedMoves:
        any_move = move_tup[0]
        any_state = move_tup[1]
        '''
    
    #findPincerMoves(newState, (1,0))
    #findQueenStyleMoves(newState, (3, 2))
    #findQueenStyleMoves(newState, (3, 4))
        
    #tup = random.choice(generatedMoves)
    #print("tuple: " + str(tup))
    #move = tup[0]
    #newState = tup[1]
    

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

# move generator for any state
def generateNewMoves(currentState, curr_player):
    gameBoard = currentState.board
    all_moves = []
    
    for row in range(8):
        for col in range(8):
            # must initialize the current player when copying state
            testState = BC.BC_state(currentState.board, curr_player)
            piece = gameBoard[row][col]
            piece_side = BC.who(piece)
            if piece_side == curr_player and not piece == 0:
                # test if piece is immobilized
                #print("location: (" + str(row) + "," + str(col) + ")")
                immobile = isPieceImmobilized(row, col, gameBoard, curr_player)
                if not immobile:
                    if piece == BC.BLACK_PINCER or piece == BC.WHITE_PINCER:
                        p_moves = findPincerMoves(testState, (row, col))
                        #print("p_moves:")
                        for move in p_moves:
                            #print()
                            #print("one move in p moves: ")
                            #for ele in move:
                                #print(str(ele))
                            all_moves.append(move)
                    elif piece == BC.BLACK_KING or piece == BC.WHITE_KING:
                        k_moves = findKingMoves(testState, (row, col))
                        #print("k_moves: ")
                        for move in k_moves:
                            #print("one move in k moves: ")
                            #for ele in move:
                            #    print(str(ele))
                            all_moves.append(move)
                    else:
                        q_moves = findQueenStyleMoves(testState, (row,col))
                        for move in q_moves:
                            all_moves.append(move)
                    # note: have not implemented IMITATOR moves yet

    return all_moves

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

# incomplete method
def findImitatorMoves(state, curr_coord):
    who = state.whose_move
    newState = BC.BC_state(state.board)
    i_moves = []
    gameBoard = state.board
    withdrawer = 0
    freezer = 0
    coordinator = 0
    king = 0
    pincer = 0
    leaper = 0

    
    

    #print("board state: ")
    #print(str(state))

    

    return i_moves

# covers coordinator, leaper, withdrawer, immobilizer
def findQueenStyleMoves(state, curr_coord):
    # deep copy the current state into a new state
    orig_board = state.board
    who = state.whose_move
    newState = BC.BC_state(orig_board, who)
    
    
    q_moves = []
    (row, col) = curr_coord
    (test_row, test_col) = curr_coord
    piece = orig_board[row][col]
    special_piece = False
    if piece == BC.BLACK_LEAPER or piece == BC.WHITE_LEAPER:
        special_piece = True

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

            if num == 0 and special_piece:
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
                    leaper_state = BC.BC_state(new_board, who)
                    leap_tup = leaperCapMove(test_row, test_col, direction, who, curr_coord, leaper_state)
                    if not leap_tup == 0:
                        new_target = leap_tup[0]
                        cap_piece = leap_tup[1]
                        new_move = (curr_coord, new_target)
                        #print("leaper state: ")
                        #print(str(leaper_state))
                        #print("captured pieces: " + str(cap_piece))
                        q_moves.append((new_move, leaper_state, cap_piece))
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
    who = state.whose_move
    newState = BC.BC_state(state.board, who)
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
                piece_cap = pincerCapMove(test_row, test_col, new_board, who)

                add_state = BC.BC_state(new_board, who)
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

# tested
def findKingMoves(state, curr_coord):
    who = state.whose_move
    newState = BC.BC_state(state.board, who)
    k_moves = []
    (king_row, king_col) = curr_coord
    piece = newState.board[king_row][king_col]
    
    piece_cap = []

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        test_piece = 99
        test_row = king_row
        test_col = king_col
        if direction == BC.NORTH:
            test_row = king_row - 1
        elif direction == BC.NE:
            test_row = king_row - 1
            test_col = king_col + 1
        elif direction == BC.EAST:
            test_col = king_col + 1
        elif direction == BC.SE:
            test_row = king_row + 1
            test_col = king_col + 1
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
                
                #print("test_row: " + str(test_row))
                #print("test_col: " + str(test_col))
                new_board[test_row][test_col] = piece
                new_board[king_row][king_col] = 0

                move = (curr_coord, (test_row, test_col))

                add_state = BC.BC_state(new_board, who)

                k_moves.append((move, add_state, piece_cap))
            elif not test_piece_side == who:
                #print("current player: " + str(who))
                #print("target location: (" + str(test_row) + "," + str(test_col) + ")")
                #print("test piece: " + str(test_piece))
                #print("test piece side: " + str(test_piece_side))
                piece_cap = []
                piece_cap.append(test_piece)

                new_board = deepcopy(newState.board)
                new_board[test_row][test_col] = piece
                new_board[king_row][king_col] = 0

                move = (curr_coord, (test_row, test_col))

                add_state = BC.BC_state(new_board, who)

                k_moves.append((move, add_state, piece_cap))
            '''else:
                print("test_piece (own side?):  " + str(test_piece))'''

    return k_moves

# this function takes a given board and captures an enemy piece via the Pincer
# attack if it is possible to according to Baroque Chess rules

# need to test this again with capturing functionality in all directions
def pincerCapMove(dest_row, dest_col, board, cur_player):
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

    move_dir = [BC.NORTH, BC.EAST, BC.SOUTH, BC.WEST]

    for direction in move_dir:
        cap_test = False
        enemy_row = dest_row
        enemy_col = dest_col
        ally_row = dest_row
        ally_col = dest_col
        ally_piece = 0
        enemy_piece = 0
        # capture test: piece one tile past is enemy piece and
        # piece one two tiles past is friendly piece
        if direction == BC.NORTH:
            #print("north")
            enemy_row = dest_row - 1
            ally_row = dest_row - 2
        elif direction == BC.EAST:
            #print("east")
            # increment east
            enemy_col = dest_col + 1
            ally_col = dest_col + 2
        elif direction == BC.SOUTH:
            #print("south")
            # increment south
            enemy_row = dest_row + 1
            ally_row = dest_row + 2
        elif direction == BC.WEST:
            #print("west")
            # increment west
            enemy_col = dest_col - 1
            ally_col = dest_col - 2

        if ally_col >= 0 and ally_col <= 7 and ally_row >= 0 and ally_row <= 7:
            ally_piece = board[ally_row][ally_col]
            enemy_piece = board[enemy_row][enemy_col]

        # print statements for testing
        '''
        print("orig_row: " + str(dest_row))
        print("orig_col: " + str(dest_col))
        print("enemy_row: " + str(enemy_row))
        print("enemy_col: " + str(enemy_col))
        print("ally_row: " + str(ally_row))
        print("ally_col: " + str(ally_col))
        print("ally_piece: " + str(ally_piece))
        print("enemy_piece: " + str(enemy_piece))
        print()
        '''

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

# tested
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

    
                
# helper method for coordCapMove
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

    
# tested, leaper can capture properly
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
    elif direction == BC.NE:
        # increment NE
        enemy_row = dest_row - 1
        empty_row = dest_row - 2
        enemy_col = dest_col + 1
        empty_col = dest_col + 2
    elif direction == BC.EAST:
        # increment east
        enemy_col = dest_col + 1
        empty_col = dest_col + 2
    elif direction == BC.SE:
        # increment SE
        enemy_row = dest_row + 1
        empty_row = dest_row + 2
        enemy_col = dest_col + 1
        empty_col = dest_col + 2
    elif direction == BC.SOUTH:
        # increment south
        enemy_row = dest_row + 1
        empty_row = dest_row + 2
    elif direction == BC.SW:
        # increment SW
        enemy_row = dest_row + 1
        empty_row = dest_row + 2
        enemy_col = dest_col - 1
        empty_col = dest_col - 2
    elif direction == BC.WEST:
        # increment west
        enemy_col = dest_col - 1
        empty_col = dest_col - 2
    elif direction == BC.NW:
        # increment NW
        enemy_row = dest_row - 1
        empty_row = dest_row - 2
        enemy_col = dest_col - 1
        empty_col = dest_col - 2

    # board boundary check
    if empty_col >= 0 and empty_col <= 7 and empty_row >= 0 and empty_row <= 7:
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
def imitatorCapMove(orig_row, orig_col, dest_row, dest_col, direction, board, cur_player):
    print("imitator doesn't know how to capture")
    # tbh i have no idea how to code this one i'll figure it out later
    #withdrawerCapMove

# tested
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
    elif direction == BC.NE:
        # test SW
        enemy_row = orig_row + 1
        enemy_col = orig_col - 1
    elif direction == BC.EAST:
        # test W
        enemy_col = orig_col - 1
    elif direction == BC.SE:
        # test NW
        enemy_row = orig_row - 1
        enemy_col = orig_col - 1
    elif direction == BC.SOUTH:
        # test N
        enemy_row = orig_row - 1
    elif direction == BC.SW:
        # test NE
        enemy_row = orig_row - 1
        enemy_col = orig_col + 1
    # below part not right
    elif direction == BC.WEST:
        # test E
        enemy_col = orig_col + 1
    elif direction == BC.NW:
        # test SE
        enemy_row = orig_row + 1
        enemy_col = orig_col + 1

    if enemy_row >= 0 and enemy_row <= 7 and enemy_col >= 0 and enemy_col <= 7:
        enemy_piece = board[enemy_row][enemy_col]

    enemy_side = BC.who(enemy_piece)

    if not enemy_side == cur_player and not enemy_piece == 0:
        cap_piece.append(enemy_piece)
        board[enemy_row][enemy_col] = 0

    return cap_piece

# helper function for testing if piece is next to another piece
def isPieceNextTo(piece_row, piece_col, board, other_piece):
    # initializing the test coordinate variables
    test_row = 99
    test_col = 99
    test_piece = 99

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        # have to initialize test_row and and test_col to their
        # default values every time
        test_piece = 99
        test_row = piece_row
        test_col = piece_col
        if direction == BC.NORTH:
            #print("north")
            test_row = piece_row - 1
        elif direction == BC.NE:
            #print("northeast")
            test_row = piece_row - 1
            test_col = piece_col + 1
        elif direction == BC.EAST:
            #print("east")
            test_col = piece_col + 1
        elif direction == BC.SE:
            #print("se")
            test_row = piece_row + 1
            test_col = piece_col + 1
        elif direction == BC.SOUTH:
            #print("s")
            test_row = piece_row + 1
        elif direction == BC.SW:
            #print("sw")
            test_row = piece_row + 1
            test_col = piece_col - 1
        elif direction == BC.WEST:
            #print("w")
            test_col = piece_col - 1
        elif direction == BC.NW:
            #print("nw")
            test_row = piece_row - 1
            test_col = piece_col - 1

        #print("test row: " + str(test_row))
        #print("test col: " + str(test_col))

        if test_row >= 0 and test_row <= 7 and test_col >=0 and test_col <= 7:
            test_piece = board[test_row][test_col]

        #print("test piece: " + str(test_piece))
        #print("other piece: " + str(other_piece))

        if test_piece == other_piece:
            return (True, direction)

    return (False, None)
    
        
def isPieceImmobilized(piece_row, piece_col, board, curr_player):
    x_val = piece_row
    y_val = piece_col
    freezer = 0

    if curr_player == BC.WHITE:
        freezer = BC.BLACK_FREEZER
    else:
        freezer = BC.WHITE_FREEZER

    (freeze_test, direction) = isPieceNextTo(x_val, y_val, board, freezer)
    #print("value of freeze test: " + str(freeze_test))

    return freeze_test
    
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

#methods required to be implemented: canMove(initial_coords,final_coords,state)
#                                    getKillList(initial_coords,final_coords,state)
def staticEval(state):
    weights = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7]
    board = state.board
    white_list = []
    black_list = []
    piece_present_sum = 0
    for i in range(0,8):
        for j in range(0,8):
            piece = board[i][j]
            if piece != 0 and piece != 1:
                if piece % 2 == 0:
                    piece_present_sum -= weights[piece]
                    black_list.append([piece,(i,j)])
                else:
                    piece_present_sum += weights[piece]
                    white_list.append([piece,(i,j)])
    to_return = 0.3*(piece_present_sum)
    move_sum = 0
    available_pieces = white_list + black_list
    for [piece,(x,y)] in available_pieces:
        for i in range(0,8):
            for j in range(0,8):
                if canMove((x,y),(i,j),state):
                    kill_list = getKillList((x,y),(i,j),state)
                    kill_sum = 0
                    for elem in kill_list:
                        kill_sum += weights[elem]
                    if not(piece % 2 == 0):
                        move_sum += kill_sum
                    else:
                        move_sum -= kill_sum
    to_return += 0.7*(move_sum)
    return to_return



