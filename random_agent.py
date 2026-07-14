"""
Random Agent for Connect Four.
CP468 - Artificial Intelligence

This agent handles:
- Legal move generation
- Random move selection
- Baseline gameplay decisions
"""
from game_engine import *
import random

class RandomAgent:
    """
    Agent 1: Random Agent

    Chooses one legal move uniformly at random.
    """

    def choose_move(self, board):
        """
        Select a random legal move.

        Args:
            board (list[list[int]]): Current game board.

        Returns:
            int: Column index of the chosen move.
        """
        moves = legal_move(board)

        if len(moves) == 0:
            return None

        return random.choice(moves)