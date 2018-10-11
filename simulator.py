import pickle
from pathlib import Path

import chess

import decision_tree
from ocean_eater_network import create_model

model = create_model()


def simulate_game(model, game_number=0, use_probabilistic_decisions=True):
    board = chess.Board()
    player_1_boards = []
    player_2_boards = []
    number_of_moves = 0

    storage_folder = Path("GameHistories")
    if not storage_folder.is_dir():
        storage_folder.mkdir()

    with open(storage_folder / ("game_history" + str(game_number) + ".txt"), 'w') as history:
        while not board.is_game_over():
            number_of_moves += 1
            is_white_turn = board.turn
            if not is_white_turn:
                board = board.mirror()

            if use_probabilistic_decisions:
                decision = decision_tree.make_probabilistic_decision(model, board)
            else:
                decision = decision_tree.make_decision(model, board)

            board.push(decision)

            if is_white_turn:
                player_1_boards.append(board)
            else:
                board = board.mirror()
                player_2_boards.append(board)

            print("Move number:", number_of_moves, file=history)
            print(board, file=history)
            print(file=history)

        print("Match outcome:", board.result(), file=history)

    with open(storage_folder / "boards.pkl", 'wb') as f:
        pickle.dump([player_1_boards, player_2_boards], f)

    return player_1_boards, player_2_boards, board
