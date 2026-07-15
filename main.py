"""
Supports:
- Human vs AI
- AI vs AI
- Random, Rule-Based, and Minimax agents
"""

from __future__ import annotations

import random
from typing import Optional

from game_engine import (
    COLUMNS,
    EMPTY,
    PLAYER1,
    PLAYER2,
    apply_move,
    create_board,
    is_terminal,
    legal_move,
    winner,
)
from minimax_agent import MinimaxAgent
from random_agent import RandomAgent
from rule_agent import RuleAgent


SYMBOLS = {
    EMPTY: ".",
    PLAYER1: "X",
    PLAYER2: "O",
}


def display_board(board: list[list[int]]) -> None:
    """Display the board in a readable console format."""
    print()
    print("  " + " ".join(str(col + 1) for col in range(COLUMNS)))
    print(" +" + "-" * (COLUMNS * 2 - 1) + "+")
    for row in board:
        print(" |" + " ".join(SYMBOLS[cell] for cell in row) + "|")
    print(" +" + "-" * (COLUMNS * 2 - 1) + "+")
    print()


def get_agent_move(agent, board: list[list[int]]) -> Optional[int]:
    """Call an agent despite the current method-name inconsistency."""
    if hasattr(agent, "get_move"):
        return agent.get_move(board)
    if hasattr(agent, "choose_move"):
        return agent.choose_move(board)
    raise TypeError(f"{type(agent).__name__} has no supported move method.")


def human_move(board: list[list[int]]) -> int:
    """Prompt until the human selects a valid, non-full column."""
    valid_moves = legal_move(board)

    while True:
        raw = input(f"Choose a column (1-{COLUMNS}): ").strip()

        try:
            column = int(raw) - 1
        except ValueError:
            print("Please enter a whole number.")
            continue

        if column not in range(COLUMNS):
            print(f"Column must be between 1 and {COLUMNS}.")
        elif column not in valid_moves:
            print("That column is full. Choose another column.")
        else:
            return column


def create_agent(choice: str, player: int, depth: int = 4):
    """Create an agent from a menu choice."""
    if choice == "1":
        return None, "Human"
    if choice == "2":
        return RandomAgent(), "Random Agent"
    if choice == "3":
        return RuleAgent(player), "Rule-Based Agent"
    if choice == "4":
        return MinimaxAgent(player, depth=depth), f"Minimax Agent (depth {depth})"
    raise ValueError("Invalid agent choice.")


def choose_player(player_number: int):
    """Display the agent-selection menu for one player."""
    print(f"\nSelect Player {player_number}:")
    print("1. Human")
    print("2. Random Agent")
    print("3. Rule-Based Agent")
    print("4. Minimax Agent")

    while True:
        choice = input("Selection: ").strip()
        if choice in {"1", "2", "3", "4"}:
            return choice
        print("Enter 1, 2, 3, or 4.")


def play_game(
    player1,
    player2,
    player1_name: str,
    player2_name: str,
    pause_ai: bool = False,
) -> Optional[int]:
    """Run one complete Connect Four game and return the winner."""
    board = create_board()
    current_player = PLAYER1

    print("\nSymbols:")
    print(f"X = Player 1 ({player1_name})")
    print(f"O = Player 2 ({player2_name})")

    while not is_terminal(board):
        display_board(board)

        current_agent = player1 if current_player == PLAYER1 else player2
        current_name = player1_name if current_player == PLAYER1 else player2_name

        print(f"Player {current_player} — {current_name}")

        if current_agent is None:
            move = human_move(board)
        else:
            move = get_agent_move(current_agent, board)
            if move is None:
                break
            print(f"{current_name} chooses column {move + 1}.")
            if pause_ai:
                input("Press Enter for the next move...")

        apply_move(board, move, current_player)
        current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1

    display_board(board)
    game_winner = winner(board)

    if game_winner == PLAYER1:
        print(f"Player 1 ({player1_name}) wins!")
    elif game_winner == PLAYER2:
        print(f"Player 2 ({player2_name}) wins!")
    else:
        print("The game is a draw.")

    return game_winner


def main() -> None:
    """Display the main menu and run games until the user exits."""
    print("=" * 42)
    print("          CP468 CONNECT FOUR AI")
    print("=" * 42)

    while True:
        print("\n1. Start a game")
        print("2. Exit")
        selection = input("Selection: ").strip()

        if selection == "2":
            print("Goodbye!")
            return

        if selection != "1":
            print("Enter 1 or 2.")
            continue

        player1_choice = choose_player(1)
        player2_choice = choose_player(2)

        player1, player1_name = create_agent(player1_choice, PLAYER1)
        player2, player2_name = create_agent(player2_choice, PLAYER2)

        pause_ai = player1 is not None and player2 is not None
        if pause_ai:
            response = input(
                "Pause after each AI move? (y/n): "
            ).strip().lower()
            pause_ai = response == "y"

        play_game(
            player1,
            player2,
            player1_name,
            player2_name,
            pause_ai=pause_ai,
        )


if __name__ == "__main__":
    main()