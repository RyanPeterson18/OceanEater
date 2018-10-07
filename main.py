import chess

from decision_tree import make_decision
from ocean_eater_network import create_model

model = create_model()
test_board = chess.Board()
make_decision(model, test_board)
