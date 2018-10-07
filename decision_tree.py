from collections import deque
import chess

COLORS = [WHITE, BLACK] = [True, False]


class DecisionTree:
    def __init__(self, board: chess.Board):
        self.board = board
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# This will create the tree of board states to traverse
# will also return list of leaf nodes
# root must always be WHITE
def create_tree(root, default_state_cap=1000):
    q = deque([root])
    # q contains all leaf nodes

    # generate tree breadth first
    while 0 < len(q) < default_state_cap:
        current_tree = q.popleft()
        for move in current_tree.board.legal_moves:
            possible_board = current_tree.board.copy()
            possible_board.push(move)
            child = DecisionTree(possible_board)
            current_tree.add_child(child)
            q.append(child)

    return q


"""

test = chess.Board()
test_tree = DecisionTree(test)
print(test_tree.board)
create_tree(test_tree)
print("Good")

"""

