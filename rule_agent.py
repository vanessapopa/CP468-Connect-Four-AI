"""
Rule-Based Agent for Connect Four.
CP468 - Artificial Intelligence

This agent handles:
- Play a winning move if available
- Block an opponent's winning move
- Prefer the center column
- Prefer moves closest to the center
"""
from game_engine import *

import copy
import random


class RuleAgent:

    def __init__(self, player):

        self.player = player

        self.opponent = (
            PLAYER1 if player == PLAYER2
            else PLAYER2
        )

    def get_move(self, board):

        moves = legal_move(board)

        # Rule 1: Play a winning move
        for move in moves:

            temp_board = copy.deepcopy(board)

            apply_move(
                temp_board,
                move,
                self.player
            )

            if check_win(
                temp_board,
                self.player
            ):
                return move

        # Rule 2: Block opponent's winning move
        for move in moves:

            temp_board = copy.deepcopy(board)

            apply_move(
                temp_board,
                move,
                self.opponent
            )

            if check_win(
                temp_board,
                self.opponent
            ):
                return move

        # Rule 3: Take the center column
        center_col = COLUMNS // 2

        if center_col in moves:
            return center_col

        # Rule 4: Prefer columns near the center
        preferred_order = [3, 2, 4, 1, 5, 0, 6]

        for move in preferred_order:
            if move in moves:
                return move

        # Fallback (should never happen)
        return random.choice(moves)