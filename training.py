import numpy as np

import decision_tree

NUMBER_OF_POSITION_STATES = 12
NUMBER_OF_PIECES = 6


def one_hot_board(board):
    if type(board) == decision_tree.DecisionTree:
        board = board.board

    raw_board = np.zeros((8, 8))
    for i in range(64):
        piece = board.piece_at(i)
        if piece is not None:
            # Set the value at the 2D index with a 1D i
            # Add 6 to the piece type if the piece is black
            raw_board[i // 8, i % 8] = piece.piece_type + \
                                       (NUMBER_OF_PIECES if not piece.color else 0)

    encoded_board = (np.arange(NUMBER_OF_POSITION_STATES) ==
                     raw_board[..., None] - 1).astype(int)
    return encoded_board


def one_hot_batch(batch):
    encoded_boards = np.zeros((len(batch), 8, 8))
    for i, board in enumerate(batch):
        encoded_boards[i] = one_hot_board(board)

    return encoded_boards
