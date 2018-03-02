import BC_state_etc as BC

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

def staticEval(state):
    #figure out whose turn it is.
    #if white's then maximize state value.
    #if black's then minimise it.
