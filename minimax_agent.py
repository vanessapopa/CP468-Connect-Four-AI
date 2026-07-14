from game_engine import *

import copy
import random

def evaluate_window(window, player):
    score = 0

    opponent = PLAYER1 if player == PLAYER2 else PLAYER2

    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty_count = window.count(EMPTY)

    # Offensive scoring
    if player_count == 4:
        score += 1000

    elif player_count == 3 and empty_count == 1:
        score += 10

    elif player_count == 2 and empty_count == 2:
        score += 5

    # Defensive scoring
    if opponent_count == 3 and empty_count == 1:
        score -= 80

    elif opponent_count == 2 and empty_count == 2:
        score -= 5

    return score

def heuristic(board, player):

    score = 0

    # Center column preference
    center_col = COLUMNS // 2

    center_values = [
        board[row][center_col]
        for row in range(ROWS)
    ]

    score += center_values.count(player) * 3

    # Horizontal
    for row in range(ROWS):

        for col in range(COLUMNS - 3):

            window = board[row][col:col + 4]

            score += evaluate_window(window, player)

    # Vertical
    for col in range(COLUMNS):

        column = [board[row][col] for row in range(ROWS)]

        for row in range(ROWS - 3):

            window = column[row:row + 4]

            score += evaluate_window(window, player)

    # Diagonal down-right
    for row in range(ROWS - 3):

        for col in range(COLUMNS - 3):

            window = [
                board[row + i][col + i]
                for i in range(4)
            ]

            score += evaluate_window(window, player)

    # Diagonal up-right
    for row in range(3, ROWS):

        for col in range(COLUMNS - 3):

            window = [
                board[row - i][col + i]
                for i in range(4)
            ]

            score += evaluate_window(window, player)

    return score

def minimax(board, depth, maximizing_player, agent_player):

    opponent = PLAYER1 if agent_player == PLAYER2 else PLAYER2

    if is_terminal(board):

        game_winner = winner(board)

        if game_winner == agent_player:
            return None, 100000

        elif game_winner == opponent:
            return None, -100000

        else:
            return None, 0

    if depth == 0:
        return None, heuristic(board, agent_player)

    legal_moves = legal_move(board)

    if maximizing_player:

        value = float("-inf")
        best_moves = []

        for move in legal_moves:

            temp_board = copy.deepcopy(board)

            apply_move(temp_board, move, agent_player)

            _, score = minimax(
                temp_board,
                depth - 1,
                False,
                agent_player
            )

            if score > value:
                value = score
                best_moves = [move]

            elif score == value:
                best_moves.append(move)

        return random.choice(best_moves), value

    else:

        value = float("inf")

        best_moves = []

        for move in legal_moves:

            temp_board = copy.deepcopy(board)

            apply_move(temp_board, move, opponent)

            _, score = minimax(
                temp_board,
                depth - 1,
                True,
                agent_player
            )

            if score < value:
                value = score
                best_moves = [move]

            elif score == value:
                best_moves.append(move)

        return random.choice(best_moves), value
    
class MinimaxAgent:

    def __init__(self, player, depth=4):

        self.player = player
        self.depth = depth

    def get_move(self, board):

        move, _ = minimax(
            board,
            self.depth,
            True,
            self.player
        )

        return move
    