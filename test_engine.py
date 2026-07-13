from game_engine import *

board = create_board()

print("Empty board:")
print_board(board)

apply_move(board, 3, PLAYER1)
apply_move(board, 3, PLAYER2)
apply_move(board, 4, PLAYER1)

print("\nBoard after moves:")
print_board(board)