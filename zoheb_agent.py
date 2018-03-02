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

    #global variables for weights of pieces

def staticEval(state):
    #list of available pieces
    #list of directions
    #to return = 0
    #piece_present_sum = 0
    #move_sum = 0
    #for list of available pieces
        #is_White = Flase;is_Black = False
        #if piece is white
            #add weight to piece_present_sum
        #else
        #remove weight from piece_present_sum
        #for all directions:
            #if can move there:
                #get final position
                #if enemy present
                    #if piece is white
                        #increment move_sum by weight
                    #else
                        #decrement move_sum by weight
    #to return = 0.7*(move_sum) + 0.3*(piece_sum)
    #return to return
    return none
