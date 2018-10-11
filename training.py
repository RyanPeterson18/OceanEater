import numpy as np

import decision_tree

NUMBER_OF_POSITION_STATES = 12
NUMBER_OF_PIECES = 6


def one_hot_board(board):
    if isinstance(board, decision_tree.DecisionTree):
        board = board.board

    def get_piece_number(i):
        piece_type = board.piece_type_at(i)
        return 0 if piece_type is None else piece_type

    raw_board = np.fromiter(map(get_piece_number, range(64)),
                            np.int32).reshape((1, 8, 8))

    encoded_board = (np.arange(NUMBER_OF_POSITION_STATES) ==
                     raw_board[..., None] - 1).astype(int)
    return encoded_board


def one_hot_batch(batch):
    encoded_boards = np.zeros((len(batch), 8, 8, NUMBER_OF_POSITION_STATES))
    for i, board in enumerate(batch):
        encoded_boards[i] = one_hot_board(board)

    return encoded_boards
