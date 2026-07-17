# CP468 Connect Four AI

A Python implementation of Connect Four featuring three agents of increasing intelligence:

- **Random Agent** - chooses uniformly from all legal moves.
- **Rule-Based Agent** - follows prioritized tactical rules.
- **Minimax Agent** - searches future game states using depth-limited Minimax and a heuristic evaluation function.


## Features

- Standard 7 column × 6 row Connect Four board
- Correct gravity based move execution
- Horizontal, vertical, and diagonal win detection
- Draw and terminal state detection
- Human vs human, human vs AI, and AI vs AI play
- Configurable Minimax search depth
- Reproducible head to head experiments using a fixed random seed
- CSV export of win rates, draw rates, and average decision times

## Requirements

- Python 3.10 or newer
- No additional Python packages are required

## Project Structure

```text
CP468-Connect-Four-AI/
├── game_engine.py       # Board representation and shared game rules
├── random_agent.py      # Uniformly random baseline agent
├── rule_agent.py        # Prioritized rule based agent
├── minimax_agent.py     # Minimax search and heuristic evaluation
├── main.py              # Command line game interface
├── experiments.py       # Required AI vs AI experimental evaluation
├── test_engine.py       # Basic engine test script
└── README.md            # Project documentation
```

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/vanessapopa/CP468-Connect-Four-AI.git
cd CP468-Connect-Four-AI
```

## Running the Game

Run the command line interface:

```bash
python main.py
```

On Windows, this command can also be used:

```bash
py main.py
```

The menu allows each side to be selected as:

1. Human
2. Random Agent
3. Rule-Based Agent
4. Minimax Agent

Board symbols:

- `X` - Player 1
- `O` - Player 2
- `.` - Empty position

Columns are entered using the numbers `1` through `7`.

## Running the Engine Test

Run the basic board and move execution test:

```bash
python test_engine.py
```

This creates an empty board, applies sample moves, and prints the resulting board.

## Running the Experiments

This assignment requires the following pairings:

- Random vs Rule-Based
- Rule-Based vs Minimax
- Minimax vs Random

Each pairing is run for 30 games, alternating which agent moves first.

The required experiments can be run with:

```bash
python experiments.py --seed 468 --games 30 --depth 4
```

The default values are seed `468`, 30 games per pairing, and Minimax depth `4`, this shorter command produces using the same set up:

```bash
python experiments.py
```

Results are printed to the console and saved to:

```text
experiment_results.csv
```

A different output filename can be selected using:

```bash
python experiments.py --output results_seed_468.csv
```

## Game Engine

The board is represented by a two dimensional Python list:

- `0` - empty cell
- `1` - Player 1
- `2` - Player 2

The shared game engine exposes:

- `create_board()` - creates an empty 6 × 7 board
- `print_board(board)` - prints the board
- `legal_move(board)` - returns all non full columns
- `apply_move(board, column, player)` - drops a disc using gravity
- `check_win(board, player)` - checks all winning directions
- `winner(board)` - returns the winning player, if there is one
- `is_draw(board)` - identifies a full board without a winner
- `is_terminal(board)` - identifies any finished game

All of the agents use this engine to ensure they follow the same rules.

## Demonstration Video

**Video:** <video controls src="https://lauriercloud-my.sharepoint.com/:v:/r/personal/popa1395_mylaurier_ca/Documents/Recordings/CP468-20260716_225811-Meeting%20Recording.mp4?csf=1&web=1&e=oFgqU9&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D" title="[Insert demonstration video link]"></video>
