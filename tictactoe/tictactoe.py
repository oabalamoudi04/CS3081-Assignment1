"""
Tic Tac Toe Player (Minimax)
"""
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    # X starts first. If equal moves -> X turn, else O turn.
    return X if count_x == count_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Does NOT modify the original board.
    """
    if action is None or len(action) != 2:
        raise Exception("Invalid action")

    i, j = action

    if i not in (0, 1, 2) or j not in (0, 1, 2):
        raise Exception("Invalid action: out of bounds")

    if board[i][j] is not EMPTY:
        raise Exception("Invalid action: cell is not empty")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one (X, O, or None).
    """
    # Rows
    for row in board:
        if row[0] is not EMPTY and row[0] == row[1] == row[2]:
            return row[0]

    # Columns
    for c in range(3):
        if board[0][c] is not EMPTY and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]

    # Diagonals
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] is not EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over (win or tie), False otherwise.
    """
    if winner(board) is not None:
        return True

    # If any empty cell exists, game is not over
    for row in board:
        if EMPTY in row:
            return False

    # No empty cells -> tie
    return True


def utility(board):
    """
    Returns 1 if X has won, -1 if O has won, 0 for tie.
    Assumes board is terminal.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action (i, j) for the current player.
    If board is terminal, returns None.
    """
    if terminal(board):
        return None

    turn = player(board)

    if turn == X:
        best_score = float("-inf")
        best_move = None
        for action in actions(board):
            score = _min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    else:
        best_score = float("inf")
        best_move = None
        for action in actions(board):
            score = _max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action
        return best_move


def _max_value(board):
    """
    Returns the max utility value from this board state (X's turn).
    """
    if terminal(board):
        return utility(board)

    v = float("-inf")
    for action in actions(board):
        v = max(v, _min_value(result(board, action)))
    return v


def _min_value(board):
    """
    Returns the min utility value from this board state (O's turn).
    """
    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, _max_value(result(board, action)))
    return v