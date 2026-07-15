"""
Each pairing runs 30 games and alternates which agent moves first.
Results are printed and saved to experiment_results.csv.
"""

from __future__ import annotations

import argparse
import csv
import platform
import random
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from game_engine import (
    PLAYER1,
    PLAYER2,
    apply_move,
    create_board,
    is_terminal,
    winner,
)
from minimax_agent import MinimaxAgent
from random_agent import RandomAgent
from rule_agent import RuleAgent


@dataclass
class TimedAgent:
    name: str
    agent: object
    total_time: float = 0.0
    move_count: int = 0

    def move(self, board) -> Optional[int]:
        start = time.perf_counter()

        if hasattr(self.agent, "get_move"):
            selected = self.agent.get_move(board)
        elif hasattr(self.agent, "choose_move"):
            selected = self.agent.choose_move(board)
        else:
            raise TypeError(
                f"{type(self.agent).__name__} has no supported move method."
            )

        self.total_time += time.perf_counter() - start
        self.move_count += 1
        return selected

    @property
    def average_time(self) -> float:
        if self.move_count == 0:
            return 0.0
        return self.total_time / self.move_count


def random_factory(player: int, depth: int):
    return RandomAgent()


def rule_factory(player: int, depth: int):
    return RuleAgent(player)


def minimax_factory(player: int, depth: int):
    return MinimaxAgent(player, depth=depth)


def play_game(agent1: TimedAgent, agent2: TimedAgent) -> Optional[int]:
    """Play one silent AI-vs-AI game."""
    board = create_board()
    current_player = PLAYER1

    while not is_terminal(board):
        current_agent = agent1 if current_player == PLAYER1 else agent2
        move = current_agent.move(board)

        if move is None:
            break

        apply_move(board, move, current_player)
        current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1

    return winner(board)


def run_pairing(
    name_a: str,
    factory_a: Callable,
    name_b: str,
    factory_b: Callable,
    games: int,
    depth: int,
) -> dict:
    """
    Run one pairing.

    Even-numbered games place Agent A first.
    Odd-numbered games place Agent B first.
    """
    wins_a = 0
    wins_b = 0
    draws = 0
    times_a = []
    times_b = []

    for game_index in range(games):
        a_first = game_index % 2 == 0

        if a_first:
            player1 = TimedAgent(name_a, factory_a(PLAYER1, depth))
            player2 = TimedAgent(name_b, factory_b(PLAYER2, depth))
        else:
            player1 = TimedAgent(name_b, factory_b(PLAYER1, depth))
            player2 = TimedAgent(name_a, factory_a(PLAYER2, depth))

        game_winner = play_game(player1, player2)

        agent_a = player1 if a_first else player2
        agent_b = player2 if a_first else player1
        times_a.extend(
            [agent_a.average_time] if agent_a.move_count else []
        )
        times_b.extend(
            [agent_b.average_time] if agent_b.move_count else []
        )

        if game_winner is None:
            draws += 1
        elif (game_winner == PLAYER1 and a_first) or (
            game_winner == PLAYER2 and not a_first
        ):
            wins_a += 1
        else:
            wins_b += 1

    return {
        "matchup": f"{name_a} vs {name_b}",
        "agent_a": name_a,
        "agent_b": name_b,
        "agent_a_wins": wins_a,
        "agent_b_wins": wins_b,
        "draws": draws,
        "agent_a_win_rate": wins_a / games,
        "agent_b_win_rate": wins_b / games,
        "draw_rate": draws / games,
        "avg_time_a_seconds": statistics.mean(times_a) if times_a else 0.0,
        "avg_time_b_seconds": statistics.mean(times_b) if times_b else 0.0,
    }


def print_results(results: list[dict], seed: int, games: int, depth: int) -> None:
    print("\nEXPERIMENT SETTINGS")
    print(f"Seed: {seed}")
    print(f"Games per pairing: {games}")
    print(f"Minimax depth: {depth}")
    print(f"Python: {platform.python_version()}")
    print(f"OS: {platform.platform()}")

    print("\nRESULTS")
    header = (
        f"{'Matchup':<29}"
        f"{'A Wins':>8}"
        f"{'B Wins':>8}"
        f"{'Draws':>8}"
        f"{'Avg A (s)':>13}"
        f"{'Avg B (s)':>13}"
    )
    print(header)
    print("-" * len(header))

    for result in results:
        print(
            f"{result['matchup']:<29}"
            f"{result['agent_a_wins']:>8}"
            f"{result['agent_b_wins']:>8}"
            f"{result['draws']:>8}"
            f"{result['avg_time_a_seconds']:>13.6f}"
            f"{result['avg_time_b_seconds']:>13.6f}"
        )


def save_results(results: list[dict], output_file: str) -> None:
    path = Path(output_file)
    fieldnames = list(results[0].keys())

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved results to: {path.resolve()}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the CP468 Connect Four AI experiments."
    )
    parser.add_argument("--seed", type=int, default=468)
    parser.add_argument("--games", type=int, default=30)
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument(
        "--output",
        default="experiment_results.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.games <= 0:
        raise ValueError("--games must be greater than zero.")
    if args.depth <= 0:
        raise ValueError("--depth must be greater than zero.")

    random.seed(args.seed)

    pairings = [
        ("Random", random_factory, "Rule-Based", rule_factory),
        ("Rule-Based", rule_factory, "Minimax", minimax_factory),
        ("Minimax", minimax_factory, "Random", random_factory),
    ]

    results = [
        run_pairing(
            name_a,
            factory_a,
            name_b,
            factory_b,
            args.games,
            args.depth,
        )
        for name_a, factory_a, name_b, factory_b in pairings
    ]

    print_results(results, args.seed, args.games, args.depth)
    save_results(results, args.output)


if __name__ == "__main__":
    main()