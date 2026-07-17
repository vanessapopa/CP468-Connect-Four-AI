from game_engine import *

board = create_board()

print("Empty board:")
print_board(board)

apply_move(board, 3, PLAYER1)
apply_move(board, 3, PLAYER2)
apply_move(board, 4, PLAYER1)
apply_move(board, 4, PLAYER2)
apply_move(board, 5, PLAYER1)
apply_move(board, 5, PLAYER2)
apply_move(board, 6, PLAYER1)  # This should create a diagonal win for PLAYER1

print("\nBoard after moves:")
print_board(board)
print("Legal moves:", legal_move(board))
print("Check draw:", is_draw(board))
print("Check win for PLAYER1:", check_win(board, PLAYER1))
print("Check win for PLAYER2:", check_win(board, PLAYER2))
print("Winner:", winner(board))
print("Is terminal:", is_terminal(board))