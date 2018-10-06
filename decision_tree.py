class DecisionTree:
    def __init__(self,
                 board,
                 default_state_cap=1000):
        self.board = board
        self.default_state_cap = default_state_cap
        self.children = []

    def add_child(self, child):
        self.children.append(child)
