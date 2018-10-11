from collections import deque

import chess
from numpy.random import choice

import ocean_eater_network

COLORS = [WHITE, BLACK] = [True, False]
DEFAULT_STATE_CAP = 10000


class DecisionTree:
    def __init__(self, board: chess.Board):
        self.value = -1  # will hold valuation determined by predict and MinMax
        self.board = board
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# This will create the tree of board states to traverse
# will also return list of leaf nodes
# root must always be WHITE
def create_tree(root, default_state_cap=DEFAULT_STATE_CAP):
    q = deque([root])
    # q contains all leaf nodes

    end = deque()  # contains all game-over states

    # generate tree breadth first
    while len(q) + len(end) < default_state_cap and 0 < len(q):
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

    q.extend(end)
    return q


# Takes a list of decision tree leaf nodes
# assigns values to them
def evaluate_leaves(model, q):
    processed = ocean_eater_network.preprocess_decision_trees(q)
    predictions = model.predict(processed)

    for i in range(len(q)):
        q[i].value = predictions[i][0]


# runs minimax, assuming leaves have been valued
def minimax(tree):
    # if WHITE turn, use max, else use min
    if len(tree.children) == 0:
        return tree.value

    elif tree.board.turn == WHITE:
        max_val = -1
        for child in tree.children:
            max_val = max(minimax(child), max_val)
        return max_val

    else:
        min_val = 1
        for child in tree.children:
            min_val = min(minimax(child), min_val)
        return min_val


# takes a model and board state, creates a decision tree and populates its values
# returns the tree
def evaluate_possible_moves(model, board):
    root = DecisionTree(board)
    evaluate_leaves(model, create_tree(root))
    minimax(root)
    return root


# takes a model and current board state in chess.Board format, returns a move
def make_decision(model, board):
    root = evaluate_possible_moves(model, board)
    max_child = get_max_child(root)
    return max_child.board.peek()


# Same, but with a probabilistic selection
def make_probabilistic_decision(model, board):
    root = evaluate_possible_moves(model, board)
    max_child = get_probabilistic_max_child(root)
    return max_child.board.peek()


# takes a fully evaluated tree and returns the child which has the maximum value
def get_max_child(root):
    max_val = -1
    max_index = 0
    for i in range(len(root.children)):
        if root.children[i].value > max_val:
            max_val = root.children[i].value
            max_index = i
    return root.children[max_index]


def get_probabilistic_max_child(root):
    # normalize the weights to [0,1] from [-1,1]
    psum = 0
    for child in root.children:
        child.value = (child.value + 1) / 2
        psum += child.value

    # make array of probabilities for numpy.random
    if psum == 0:
        n = len(root.children)
        p = [1 / n for _ in range(n)]
    else:
        p = [child.value / psum for child in root.children]

    return choice(root.children, p=p)


""""

# test code for

model = create_model()
board = chess.Board()
root = DecisionTree(board)
evaluate_possible_moves(model, root)


# Test Code: 

test = chess.Board()
test_tree = DecisionTree(test)
print(test_tree.board)
create_tree(test_tree)
print("Good")
"""""
