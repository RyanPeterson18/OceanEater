import numpy as np
from tqdm import tqdm

from ocean_eater_network import create_model
from simulator import simulate_game
from training import one_hot_batch


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


model = create_model()
player_1_boards = []
player_2_boards = []
player_1_y = []
player_2_y = []
final_boards = []
results = []

for i in tqdm(range(10)):
    p1_boards, p2_boards, final_board = simulate_game(model)

    result = final_board.result()
    results.append(result)

    p1_y = np.ones((len(p1_boards),))
    p2_y = np.ones((len(p2_boards),))
    if result == '1-0':
        p2_y *= -1
    elif result == '0-1':
        p1_y *= -1
    else:
        p2_y -= 1
        p1_y -= 1

    player_1_boards.append(one_hot_batch(p1_boards))
    player_2_boards.append(one_hot_batch(p2_boards))

    player_1_y.append(p1_y)
    player_2_y.append(p2_y)

player_1_boards = np.concatenate(tuple(player_1_boards))
player_2_boards = np.concatenate(tuple(player_2_boards))
player_1_y = np.concatenate(tuple(player_1_y))
player_2_y = np.concatenate(tuple(player_2_y))

player_boards = np.concatenate((player_1_boards, player_2_boards))
player_y = np.concatenate((player_1_y, player_2_y))

player_boards, player_y = unison_shuffled_copies(player_boards, player_y)

model.compile(optimizer='rmsprop', loss='mean_squared_error')

print("Starting loss:", model.evaluate(player_boards, player_y))

model.fit(player_boards, player_y, batch_size=32)

print("Final loss:", model.evaluate(player_boards, player_y))