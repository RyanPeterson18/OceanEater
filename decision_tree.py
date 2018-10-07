from collections import deque
import chess

COLORS = [WHITE, BLACK] = [True, False]


class DecisionTree:
    def __init__(self, board: chess.Board):
        self.best_score = -1  # will hold valuation determined by predict and MinMax
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

    end = deque()  # contains all game-over states

    # generate tree breadth first
    while 0 < len(q) + len(end) < default_state_cap:
        current_tree = q.popleft()
        if current_tree.board.is_game_over():
            end.append(current_tree)
        else:
            for move in current_tree.board.legal_moves:
                possible_board = current_tree.board.copy()
                possible_board.push(move)
                child = DecisionTree(possible_board)
                current_tree.add_child(child)
                q.append(child)

    return q.extend(end)


""""

# Test Code: 

test = chess.Board()
test_tree = DecisionTree(test)
print(test_tree.board)
create_tree(test_tree)
print("Good")

"""""


# Takes a list of decision tree leaf nodes
# assigns values to them
def evaluate_leaves(model, q):
    for tree in q:
        tree.best_score = model.predict(tree.board)


# assuming all leaves have values, propagate the values upwards using minimax
def minimax(root):
    d = deque(root)
    while len(d) > 0:
        current_tree = d[-1]
        if len(current_tree.children) == 0:

            for child in current_tree.children:
                d.append(child)


def value(tree):
    # if WHITE turn, use max, else use min
    if len(tree.children) == 0:
        return tree.best_score

    elif tree.board.turn == WHITE:
        max_val = -1
        for child in tree.children:
            max_val = max(value(child), max_val)
        return max_val

    else:
        min_val = 1
        for child in tree.children:
            min_val = min(value(child), min_val)
        return min_val
