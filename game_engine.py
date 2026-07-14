"""
Game engine for Connect Four.
CP468 - Aritificial Intelligence

This file handles:
- Board representation
- Legal move generation
- Move execution
- Win detection
- Draw detection
"""

# CONSTANTS
ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

# BOARD FUNCTIONS
def create_board():
    """
    Create a new empty Connect Four board.
    
    Returns:
        list[list[int]]: A 6x7 board filled with EMPTY (0).
    """
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """
    Print the Connect Four board to the console.
    """
    for row in board:
        print(row)

def legal_move(board):
    """
    Returns a list of columns that are not full.
    """
    moves = []
    for col in range(COLUMNS):
        if board[0][col] == EMPTY:
            moves.append(col)
    return moves

def apply_move(board, col, player):
    """
    Drops a player's piece into a column.
    
    Returns:
        TRUE if move is successful,
        FALSE if the column is full.
    """
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """
    Checks if the player has won the game.
    """

    # HORIZONTAL CHECK
    for row in range(ROWS):
        for col in range(COLUMNS - 3):

            if (
                board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player
            ):
                return True
    
    # VERTICAL CHECK
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if (
                board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player
            ):
                return True

    # DIAGONAL DOWN-RIGHT CHECK
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (
                board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player
            ):
                return True
    
    # DIAGONAL UP-RIGHT CHECK
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (
                board[row][col] == player and
                board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player
            ):
                return True

    return False

def winner(board):
    """
    Returns the winner of the game, if any.
    """
    if check_win(board, PLAYER1):
        return PLAYER1
    elif check_win(board, PLAYER2):
        return PLAYER2
    else:
        return None

def is_draw(board):
    """
    Returns TRUE if the game is a draw
    """
    return winner(board) is None and len(legal_move(board)) == 0

def is_terminal(board):
    """
    Returns TRUE if the game is over (win or draw)
    """
    return winner(board) is not None or is_draw(board)