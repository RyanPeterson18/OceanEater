import chess
import numpy as np
from sklearn.preprocessing import OneHotEncoder

NUMBER_OF_POSITION_STATES = 13
_ENCODER = OneHotEncoder(categories=13)


def one_hot_board(board: chess.Board):
    raw_board = np.zeros((8, 8))
    for i in range(64):
        piece = board.piece_at(i)
        if piece is not None:
            raw_board[i // 8, i % 8] = piece.piece_type

    encoded_board = (np.arange(raw_board.max()) == raw_board[..., None] - 1).astype(int)
    return encoded_board


def one_hot_batch(batch):
    raw_boards = np.zeros((len(batch), 8, 8))
    for i in range(len(batch)):
        raw_boards[i] = one_hot_board(batch[i])

    encoded_boards = _ENCODER.transform(batch)
    return encoded_boards
