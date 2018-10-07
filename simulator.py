import chess

from ocean_eater_network import create_model

model = create_model()
board = chess.Board()

while not board.is_game_over():
    model.predict()
