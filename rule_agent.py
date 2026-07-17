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
    def __init__(self, player: int):
        self.player = player
        self.opponent = PLAYER1 if player == PLAYER2 else PLAYER2

    def _open_line_score(self, board) -> int:
        """
        Score windows that contain the agent's pieces and no opponent pieces.
        Higher scores favour longer lines and immediate threats.
        """
        score = 0
        windows = []

        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                windows.append(board[row][col : col + 4])

        for col in range(COLUMNS):
            column = [board[row][col] for row in range(ROWS)]
            for row in range(ROWS - 3):
                windows.append(column[row : row + 4])

        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                windows.append(
                    [board[row + i][col + i] for i in range(4)]
                )

        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                windows.append(
                    [board[row - i][col + i] for i in range(4)]
                )

        for window in windows:
            if self.opponent not in window:
                own_count = window.count(self.player)
                empty_count = window.count(EMPTY)

                if own_count == 3 and empty_count == 1:
                    score += 100
                elif own_count == 2 and empty_count == 2:
                    score += 10
                elif own_count == 1 and empty_count == 3:
                    score += 1

        return score

    def _winning_moves(self, board, player: int, moves: list[int]) -> list[int]:
        winning = []

        for move in moves:
            temp_board = copy.deepcopy(board)
            apply_move(temp_board, move, player)

            if check_win(temp_board, player):
                winning.append(move)

        return winning

    def get_move(self, board):
        moves = legal_move(board)

        if not moves:
            return None

        # Rule 1: play an immediate winning move.
        winning_moves = self._winning_moves(board, self.player, moves)
        if winning_moves:
            return random.choice(winning_moves)

        # Rule 2: block an immediate opponent win.
        blocking_moves = self._winning_moves(board, self.opponent, moves)
        if blocking_moves:
            return random.choice(blocking_moves)

        # Rule 3: take the centre column.
        centre = COLUMNS // 2
        if centre in moves:
            return centre

        # Rule 4: extend/create the strongest open line.
        scored_moves = {}
        for move in moves:
            temp_board = copy.deepcopy(board)
            apply_move(temp_board, move, self.player)
            scored_moves[move] = self._open_line_score(temp_board)

        best_score = max(scored_moves.values())
        best_moves = [
            move for move, score in scored_moves.items()
            if score == best_score
        ]

        if best_score > 0:
            return random.choice(best_moves)

        # Rule 5: prefer columns closest to the centre.
        minimum_distance = min(abs(move - centre) for move in moves)
        closest_moves = [
            move for move in moves
            if abs(move - centre) == minimum_distance
        ]
        return random.choice(closest_moves)