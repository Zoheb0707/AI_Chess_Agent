import BC_state_etc as BC
from pdb import set_trace as st

def makeMove(currentState, currentRemark, timelimit):
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

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

#choose a nickname to return.
def nickname():
    return "Newman"

#select a name for the agent
def introduce():
    return "I'm the agent, a Baroque Chess agent."

def prepare(player2Nickname):
    pass

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
