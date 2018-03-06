'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''



import BC_state_etc as BC
from copy import deepcopy
import random

INVALID_PIECE = 99
BLANK_SPACE = 0

def makeMove(currentState, currentRemark, timelimit):

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    curr_player = currentState.whose_move
    newState = BC.BC_state(currentState.board, curr_player)
    
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
    #findPincerMoves(newState, (3,3))
    #findImitatorMoves(newState, (2,6))
    tup = random.choice(generatedMoves)
    #print("tuple: " + str(tup))
    move = tup[0]
    newState = tup[1]
    

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    #move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

# move generator for any state
def generateNewMoves(currentState, curr_player):
    global BLANK_SPACE
    
    gameBoard = currentState.board
    all_moves = []
    
    for row in range(8):
        for col in range(8):
            # must initialize the current player when copying state
            testState = BC.BC_state(currentState.board, curr_player)
            piece = gameBoard[row][col]
            piece_side = BC.who(piece)
            if piece_side == curr_player and not piece == BLANK_SPACE:
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
                    elif piece == BC.BLACK_IMITATOR or piece == BC.WHITE_IMITATOR:
                        i_moves = findImitatorMoves(testState, (row, col))
                        for move in i_moves:
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

# tested method
def findImitatorMoves(state, curr_coord):
    who = state.whose_move
    newState = BC.BC_state(state.board, who)
    i_moves = []
    gameBoard = state.board

    queenLikeMoves = findQueenStyleMoves(newState, curr_coord)
    for move_q in queenLikeMoves:
        i_moves.append(move_q)
        
    kingLikeMoves = findKingMoves(newState, curr_coord)
    for move_k in kingLikeMoves:
        i_moves.append(move_k)

    return i_moves

# covers coordinator, leaper, withdrawer, immobilizer
def findQueenStyleMoves(state, curr_coord):
    global BLANK_SPACE
    
    # deep copy the current state into a new state
    orig_board = state.board
    who = state.whose_move
    newState = BC.BC_state(orig_board, who)
    
    q_moves = []
    (row, col) = curr_coord
    (test_row, test_col) = curr_coord
    piece = orig_board[row][col]
    leaper = False
    coordinator = False
    withdrawer = False
    imitator = False
    if piece == BC.BLACK_LEAPER or piece == BC.WHITE_LEAPER:
        leaper = True
    elif piece == BC.BLACK_COORDINATOR or piece == BC.WHITE_COORDINATOR:
        coordinator = True
    elif piece == BC.BLACK_WITHDRAWER or piece == BC.WHITE_WITHDRAWER:
        withdrawer = True
    elif piece == BC.BLACK_IMITATOR or piece == BC.WHITE_IMITATOR:
        imitator = True

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        test_row = row
        test_col = col
        same_location = False
        pincer_direction = False
        if direction == BC.NORTH or direction == BC.EAST or direction == BC.SOUTH\
           or direction == BC.WEST:
            pincer_direction = True
        
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

            if num == 0 and (leaper or imitator):
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
            if orig_board[test_row][test_col] == BLANK_SPACE or same_location:
                # do something

                # deep copy the lists of lists
                new_board = deepcopy(newState.board)

                # default non capturing move (moving into a blank space)
                if not same_location:
                    new_board[test_row][test_col] = piece
                    new_board[row][col] = BLANK_SPACE

                cap_pieces = []

                ### capture enemy piece if possible
                if imitator:
                    # preparing the imitator capture move for the types of capture
                    leaper_state = BC.BC_state(new_board, who)
                    leap_tup = leaperCapMove(test_row, test_col, direction, who, curr_coord, leaper_state)
                    # leap_tup being equal to 0 indicates that imitator cannot act as a leaper to
                    # capture an enemy leaper
                    if not leap_tup == 0:
                        new_target = leap_tup[0]
                        cap_piece = leap_tup[1]
                        new_move = (curr_coord, new_target)
                        q_moves.append((new_move, leaper_state, cap_piece))

                    if not same_location:
                        # these pieces must move to a blank space without jumping in order to capture!
                        if pincer_direction:
                            cap_pieces = pincerCapMove(test_row, test_col, new_board, who)

                        # base case
                        c_cap_pieces = coordCapMove(test_row, test_col, new_board, who)
                        for piece_c in c_cap_pieces:
                            cap_pieces.append(piece_c)
                        
                        w_cap_pieces = withdrawerCapMove(row, col, test_row, test_col, direction, new_board, who)
                        for piece_w in w_cap_pieces:
                            cap_pieces.append(piece_w)
                    
                elif coordinator:
                    # coordinator code
                    cap_pieces = coordCapMove(test_row, test_col, new_board, who)

                    #print("captured pieces: " + str(cap_pieces))
                # leaper may change target location
                elif leaper:
                    # leaper code

                    # create new state to add to q moves potentially
                    leaper_state = BC.BC_state(new_board, who)
                    leap_tup = leaperCapMove(test_row, test_col, direction, who, curr_coord, leaper_state)

                    if not (leap_tup == 0):
                        new_target = leap_tup[0]
                        cap_piece = leap_tup[1]
                        new_move = (curr_coord, new_target)
                        q_moves.append((new_move, leaper_state, cap_piece))
                elif withdrawer:
                    # withdrawer code
                    cap_pieces = withdrawerCapMove(row, col, test_row, test_col, direction, new_board, who)
                

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

# won't return moves if called on a piece from the enemy side
def findPincerMoves(state, curr_coord):
    global BLANK_SPACE
    
    p_moves = []
    orig_board = state.board
    (row, col) = curr_coord
    piece = orig_board[row][col]
    who = state.whose_move

    piece_side = BC.who(piece)
    
    if piece_side == who: 
        newState = BC.BC_state(state.board, who)
        #print("who am i: " + str(who))
        
        (test_row, test_col) = curr_coord
        

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
                if orig_board[test_row][test_col] == BLANK_SPACE:

                    # deep copy the lists of lists
                    new_board = deepcopy(newState.board)
                    new_board[test_row][test_col] = piece
                    new_board[row][col] = BLANK_SPACE

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
    global INVALID_PIECE, BLANK_SPACE
    
    who = state.whose_move
    
    newState = BC.BC_state(state.board, who)
    k_moves = []
    (king_row, king_col) = curr_coord
    piece = newState.board[king_row][king_col]
    
    piece_cap = []

    ally_king = INVALID_PIECE
    ally_imitator = INVALID_PIECE
    enemy_king = INVALID_PIECE

    if who == BC.WHITE:
        ally_king = BC.WHITE_KING
        ally_imitator = BC.WHITE_IMITATOR
        enemy_king = BC.BLACK_KING
    else:
        ally_king = BC.BLACK_KING
        ally_imitator = BC.BLACK_IMITATOR
        enemy_king = BC.WHITE_KING
    

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        test_piece = INVALID_PIECE
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

        if not test_piece == INVALID_PIECE:
            if test_piece == BLANK_SPACE:
                if piece == ally_king:
                    piece_cap = []

                    new_board = deepcopy(newState.board)
                    
                    #print("test_row: " + str(test_row))
                    #print("test_col: " + str(test_col))
                    new_board[test_row][test_col] = piece
                    new_board[king_row][king_col] = BLANK_SPACE

                    move = (curr_coord, (test_row, test_col))

                    add_state = BC.BC_state(new_board, who)

                    k_moves.append((move, add_state, piece_cap))
            elif not test_piece_side == who:
                #print("current player: " + str(who))
                #print("target location: (" + str(test_row) + "," + str(test_col) + ")")
                #print("test piece: " + str(test_piece))
                #print("test piece side: " + str(test_piece_side))
                if piece == ally_king:
                    piece_cap = []
                    piece_cap.append(test_piece)

                    new_board = deepcopy(newState.board)
                    new_board[test_row][test_col] = piece
                    new_board[king_row][king_col] = BLANK_SPACE

                    move = (curr_coord, (test_row, test_col))

                    add_state = BC.BC_state(new_board, who)

                    k_moves.append((move, add_state, piece_cap))
                elif piece == ally_imitator:
                    if test_piece == enemy_king:
                        piece_cap = []
                        piece_cap.append(test_piece)

                        new_board = deepcopy(newState.board)
                        new_board[test_row][test_col] = piece
                        new_board[king_row][king_col] = BLANK_SPACE

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
    global INVALID_PIECE, BLANK_SPACE
    
    # test if this is a capture move or not
    #print("who am i (2): " + str(cur_player))
    enemy_row = dest_row
    enemy_col = dest_col
    ally_row = dest_row
    ally_col = dest_col
    # set ally piece and enemy piece to default blank spaces
    ally_piece = BLANK_SPACE
    enemy_piece = BLANK_SPACE
    cap_test = False
    # default captured piece is empty list
    captured_pieces = []

    # initializing pieces for testing
    pieceUsed = board[dest_row][dest_col]
    enemy_pincer = INVALID_PIECE
    ally_imitator = INVALID_PIECE
    ally_pincer = INVALID_PIECE

    if cur_player == BC.WHITE:
        enemy_pincer = BC.BLACK_PINCER
        ally_imitator = BC.WHITE_IMITATOR
        ally_pincer = BC.WHITE_PINCER
    else:
        enemy_pincer = BC.WHITE_PINCER
        ally_imitator = BC.BLACK_IMITATOR
        ally_pincer = BC.BLACK_PINCER

    # testing if piece used for capture is a pincer or a chameleon

    move_dir = [BC.NORTH, BC.EAST, BC.SOUTH, BC.WEST]

    for direction in move_dir:
        cap_test = False
        enemy_row = dest_row
        enemy_col = dest_col
        ally_row = dest_row
        ally_col = dest_col
        ally_piece = INVALID_PIECE
        enemy_piece = INVALID_PIECE
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

        # if friend and enemy are not invalid pieces
        if not ally_piece == BLANK_SPACE and not enemy_piece == BLANK_SPACE:
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
            if pieceUsed == ally_pincer:
                # capture enemy piece
                captured_pieces.append(enemy_piece)
                board[enemy_row][enemy_col] = BLANK_SPACE
            elif pieceUsed == ally_imitator:
                if enemy_piece == enemy_pincer:
                    # capture enemy piece
                    captured_pieces.append(enemy_piece)
                    board[enemy_row][enemy_col] = BLANK_SPACE

    return captured_pieces

# accounts for imitator as well as coordinator
def coordCapMove(dest_row, dest_col, board, cur_player):
    # intersection of king's rank and coordinator's file and coordinator's file
    # and king's rank are captured

    global BLANK_SPACE, INVALID_PIECE

    # pieces captured is initialized to an empty list
    captured_pieces = []

    # coordinator or imitator
    pieceUsed = board[dest_row][dest_col]

    # initialize enemy coord
    enemy_coord = INVALID_PIECE
    ally_imitator = INVALID_PIECE
    ally_coord = INVALID_PIECE

    if cur_player == BC.WHITE:
        enemy_coord = BC.BLACK_COORDINATOR
        ally_imitator = BC.WHITE_IMITATOR
        ally_coord = BC.WHITE_COORDINATOR
    else:
        enemy_coord = BC.WHITE_COORDINATOR
        ally_imitator = BC.BLACK_IMITATOR
        ally_coord = BC.BLACK_COORDINATOR

    (row_king, col_king) = findAllyKing(board, cur_player)

    # possible captured pieces
    cap_piece1 = board[row_king][dest_col]
    cap_piece2 = board[dest_row][col_king]

    #print("captured_piece1: " + str(cap_piece1))
    #print("captured_piece2: " + str(cap_piece2))

    # side of captured pieces
    piece1_side = BC.who(cap_piece1)
    piece2_side = BC.who(cap_piece2)

    if pieceUsed == ally_coord:
        # if captured piece 1 is an enemy, capture it!
        if not piece1_side == cur_player and not cap_piece1 == BLANK_SPACE:
            captured_pieces.append(cap_piece1)
            board[row_king][dest_col] = BLANK_SPACE

        # if captured piece 2 is an enemy, capture it!
        if not piece2_side == cur_player and not cap_piece2 == BLANK_SPACE:
            captured_pieces.append(cap_piece2)
            board[dest_row][col_king] = BLANK_SPACE
            
    elif pieceUsed == ally_imitator:
        # if imitator can imitate an enemy coordinator
        if cap_piece1 == enemy_coord:
            captured_pieces.append(cap_piece1)
            board[row_king][dest_col] = BLANK_SPACE

        elif cap_piece2 == enemy_coord:
            captured_pieces.append(cap_piece2)
            board[dest_row][col_king] = BLANK_SPACE
            
        
    return captured_pieces

    
                
# helper method for coordCapMove
def findAllyKing(test_board, who):
    global INVALID_PIECE
    
    # assign king to invalid piece as default
    king = INVALID_PIECE

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

    global BLANK_SPACE, INVALID_PIECE
    

    # test if this is a capture move or not
    enemy_row = dest_row
    enemy_col = dest_col
    empty_row = dest_row
    empty_col = dest_col
    # set ally piece and enemy piece to default invalid values
    empty_piece = INVALID_PIECE
    enemy_piece = INVALID_PIECE
    cap_test = False
    board = new_state.board
    piece = board[dest_row][dest_col]
    # default captured piece is empty list
    captured_pieces = []

    enemy_leaper = INVALID_PIECE
    ally_imitator = INVALID_PIECE
    ally_leaper = INVALID_PIECE

    if cur_player == BC.WHITE:
        enemy_leaper = BC.BLACK_LEAPER
        ally_imitator = BC.WHITE_IMITATOR
        ally_leaper = BC.WHITE_LEAPER
    else:
        enemy_leaper = BC.BLACK_LEAPER
        ally_imitator = BC.WHITE_IMITATOR
        ally_leaper = BC.WHITE_LEAPER

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
    if not empty_piece == INVALID_PIECE and not enemy_piece == INVALID_PIECE:
        enemy_side = BC.who(enemy_piece)
        # if other space is empty, and the
        # captured piece is an enemy
        if empty_piece == BLANK_SPACE and not enemy_side == cur_player and not enemy_piece == BLANK_SPACE:
            cap_test = True

    if cap_test:
        if piece == ally_leaper:
            new_board = new_state.board
            #print("piece: " + str(piece))
            new_board[empty_row][empty_col] = piece
            new_board[dest_row][dest_col] = BLANK_SPACE
            captured_pieces.append(enemy_piece)
            new_board[enemy_row][enemy_col] = BLANK_SPACE
            # return the new target location and captured piece (board has been modified in place)
            return ((empty_row, empty_col), captured_pieces)
        elif piece == ally_imitator:
            if enemy_piece == enemy_leaper:
                new_board = new_state.board
                #print("piece: " + str(piece))
                new_board[empty_row][empty_col] = piece
                new_board[dest_row][dest_col] = BLANK_SPACE
                captured_pieces.append(enemy_piece)
                new_board[enemy_row][enemy_col] = BLANK_SPACE
                # return the new target location and captured piece (board has been modified in place)
                return ((empty_row, empty_col), captured_pieces)

    return 0


# tested
def withdrawerCapMove(orig_row, orig_col, dest_row, dest_col, direction, board, cur_player):
    # if enemy was directly adjacent to withdrawer in the opposite direction of
    # withdrawer's movement, the enemy is captured

    # board will be modified in place (no need for a deep copy of the state)

    global INVALID_PIECE, BLANK_SPACE

    enemy_row = orig_row
    enemy_col = orig_col
    enemy_piece = INVALID_PIECE
    cap_piece = []

    # initializing pieces
    pieceUsed = board[dest_row][dest_col]
    ally_withdrawer = INVALID_PIECE
    ally_imitator = INVALID_PIECE
    enemy_withdrawer = INVALID_PIECE

    if cur_player == BC.WHITE:
        ally_withdrawer = BC.WHITE_WITHDRAWER
        ally_imitator = BC.WHITE_IMITATOR
        enemy_withdrawer = BC.BLACK_WITHDRAWER
    else:
        ally_withdrawer = BC.BLACK_WITHDRAWER
        ally_imitator = BC.BLACK_IMITATOR
        enemy_withdrawer = BC.WHITE_WITHDRAWER
    
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

    if not enemy_side == cur_player and not enemy_piece == INVALID_PIECE:
        if pieceUsed == ally_withdrawer:
            cap_piece.append(enemy_piece)
            board[enemy_row][enemy_col] = BLANK_SPACE
        elif pieceUsed == ally_imitator:
            if enemy_piece == enemy_withdrawer:
                cap_piece.append(enemy_piece)
                board[enemy_row][enemy_col] = BLANK_SPACE

    return cap_piece

# helper function for testing if piece is next to another piece
def isPieceNextTo(piece_row, piece_col, board, other_piece):
    global BLANK_SPACE, INVALID_PIECE
    
    # initializing the test coordinate variables
    test_row = 0
    test_col = 0
    test_piece = INVALID_PIECE

    move_dir = [BC.NORTH, BC.NE, BC.EAST, BC.SE, BC.SOUTH, BC.SW, BC.WEST, BC.NW]

    for direction in move_dir:
        # have to initialize test_row and and test_col to their
        # default values every time
        test_piece = INVALID_PIECE
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
    global INVALID_PIECE
    
    x_val = piece_row
    y_val = piece_col
    freezer = INVALID_PIECE

    if curr_player == BC.WHITE:
        freezer = BC.BLACK_FREEZER
    else:
        freezer = BC.WHITE_FREEZER

    (freeze_test, direction) = isPieceNextTo(x_val, y_val, board, freezer)

    return freeze_test
    
# have not implemented test for determining whether the king is in check or not
#def isKingInCheck(state):

# add possible pieces that can be killed in a given move to the tuple returned
def canMove(curr_coord, final_coord, state):
    global INVALID_PIECE, BLANK_SPACE
    
    move_test = False
    (row, col) = curr_coord
    piece = state.board[row][col]

    piece_side = BC.who(piece)

    ally_pincer = INVALID_PIECE
    ally_king = INVALID_PIECE
    ally_imitator = INVALID_PIECE
    

    if piece_side = BC.WHITE:
        ally_pincer = BC.WHITE_PINCER
        ally_king = BC.WHITE_KING
        ally_imitator = BC.WHITE_IMITATOR
    else:
        ally_pincer = BC.BLACK_PINCER
        ally_king = BC.BLACK_KING
        ally_imitator = BC.BLACK_IMITATOR
        
    
    # requested move
    req_move = (curr_coord, final_coord)

    moves = []
    if piece == BLANK_SPACE:
        return move_test
    elif piece == ally_pincer:
        moves = findPincerMoves(state, curr_coord)
    elif piece == ally_king:
        moves = findKingMoves(state, curr_coord)
    elif piece == ally_imitator:
        moves = findImitatorMoves(state, curr_coord)
    else:
        moves = findQueenStyleMoves(state, curr_coord)

    for tup in moves:
        test_move = tup[0]
        kill_list = tup[2]
        if req_move == move:
            move_test = True
            return (move_test, kill_list)

    return (move_test, None)

#methods required to be implemented: canMove(initial_coords,final_coords,state)
#                                    getKillList(initial_coords,final_coords,state)
# implemented getKillList in canMove
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
                (move_test, kill_list) = canMove((x,y),(i,j),state)
                if move_test:
                    kill_sum = 0
                    for elem in kill_list:
                        kill_sum += weights[elem]
                    if not(piece % 2 == 0):
                        move_sum += kill_sum
                    else:
                        move_sum -= kill_sum
    to_return += 0.7*(move_sum)
    return to_return

#returns (None,None) it time runs out. Else returns a static eval value and a move.
def miniMax(current_state, whos_turn, ply_left,start_time,time_limit):
    if(time.time - start.time < time_limit):
        curr_coords = (0,0)
        final_coords = (0,0)
        if ply_left == 0:
            prov = staticEval(current_state)
            move = (curr_coords, final_coords)
            return (prov,move)
        prov = 0
        if whos_turn == 'W': prov = -10000 #if white then maximize.
        else: prov = 10000
        next_turn = 0
        if whos_turn == 0: next_turn == 1
        for s in generateNewMoves(current_state,whos_turn);
            curr_coords = s[1][0]
            final_coords = s[1][1]
            (new_val,test_move) = miniMax(s[2], next_turn, ply_left - 1,start_time,time_limit)
            if (new_val != None and move != None):
                if (whos_turn == 'W' and new_val > prov) or\
                (whos_turn == 'B'and new_val < prov):
                    prov = new_val
                    move = (curr_coords,final_coords)
        return (prov,move)
    else: return (None,None)

#returns (None,None) if no time left. else returns a static eval value and a move. 
def IDDFS(current_state, whos_turn, time_limit):
    plyLeft = 0
    minimax_value = (None,None)
    start_time = time.time
    while (time.time - start_time < time_limit):
        new_value = miniMax(current_state,whos_turn,plyLeft,start_time,time_limit)
        if new_value != (None,None):
            minimax_value = new_value
        plyLeft += 1
    return minimax_value




