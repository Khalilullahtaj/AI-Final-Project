import random
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """Returns the starting state of the Tic Tac Toe board."""
    return [[EMPTY, EMPTY, EMPTY] for _ in range(3)]


def player(board):
    """Returns the player who has the next turn on a given board."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X


def actions(board):
    """Returns all available actions (empty spaces) on the board as a set of tuples."""
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """Returns the board that results from making move (i, j) on the board."""
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """Returns the winner of the game, if there is one."""
    lines = [
        # Horizontal
        [board[i][j] for j in range(3)] for i in range(3)
    ] + [
        # Vertical
        [board[i][j] for i in range(3)] for j in range(3)
    ] + [
        # Diagonals
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)]
    ]

    for line in lines:
        if line[0] == line[1] == line[2] != EMPTY:
            return line[0]
    return None


def terminal(board):
    """Returns True if game is over, otherwise False."""
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)


def utility(board):
    """Returns 1 if X has won, -1 if O has won, 0 otherwise."""
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """Returns the optimal action for the current player on the board."""
    if terminal(board):
        return None

    if player(board) == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    best_move = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v, best_move = min_val, action
            if v == 1:
                break
    return v, best_move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    best_move = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v, best_move = max_val, action
            if v == -1:
                break
    return v, best_move
