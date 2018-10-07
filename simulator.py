import chess

from decision_tree import create_tree, make_probabilistic_decision
from ocean_eater_network import create_model

model = create_model()


def simulate_game(model):
    board = chess.Board()
    player_1_boards = []
    player_2_boards = []
    number_of_moves = 0

    with open("game_history.txt", 'w') as history:
        while not board.is_game_over():
            number_of_moves += 1
            is_white_turn = board.turn
            if not is_white_turn:
                board = board.mirror()

            decision = make_probabilistic_decision(model, board)
            board.push(decision)

            if is_white_turn:
                player_1_boards.append(board)
            else:
                board = board.mirror()
                player_2_boards.append(board)

            print("Move number:", number_of_moves, file=history)
            print(board, file=history)
            print(file=history)

    return player_1_boards, player_2_boards, board
