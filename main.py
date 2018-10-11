import os

import keras
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tqdm import tqdm

from ocean_eater_network import create_model
from simulator import simulate_game
from training import one_hot_batch

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

EARLY_STOPPING = EarlyStopping(monitor='loss', patience=5)
MODEL_CHECKPOINTER = ModelCheckpoint("GameHistories/model.h5", monitor='loss')


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def play_n_games(n, model):
    player_1_boards = []
    player_2_boards = []
    player_1_y = []
    player_2_y = []
    final_boards = []
    results = []
    white_wins = 0
    black_wins = 0
    draws = 0

    for i in tqdm(range(n)):
        p1_boards, p2_boards, final_board = simulate_game(model, i)

        result = final_board.result()
        results.append(result)

        p1_y = np.ones((len(p1_boards),))
        p2_y = np.ones((len(p2_boards),))
        if result == '1-0':
            white_wins += 1
            p2_y *= -1
        elif result == '0-1':
            black_wins += 1
            p1_y *= -1
        else:
            draws += 1
            p2_y -= 1
            p1_y -= 1

        player_1_boards.append(one_hot_batch(p1_boards))
        player_2_boards.append(one_hot_batch(p2_boards))

        player_1_y.append(p1_y)
        player_2_y.append(p2_y)

    print("Number of white wins:", white_wins)
    print("Number of black wins:", black_wins)
    print("Number of draws:", draws)

    player_1_boards = np.concatenate(tuple(player_1_boards))
    player_2_boards = np.concatenate(tuple(player_2_boards))
    player_1_y = np.concatenate(tuple(player_1_y))
    player_2_y = np.concatenate(tuple(player_2_y))

    player_boards = np.concatenate((player_1_boards, player_2_boards))
    player_y = np.concatenate((player_1_y, player_2_y))

    player_boards, player_y = unison_shuffled_copies(player_boards, player_y)

    return player_boards, player_y


def training_iteration(model, number_of_games=64):
    preprocessed_player_boards, player_y = play_n_games(number_of_games, model)

    print("Starting loss:", model.evaluate(preprocessed_player_boards, player_y, verbose=0))

    model.fit(preprocessed_player_boards, player_y, batch_size=32, epochs=100,
              callbacks=[EARLY_STOPPING, MODEL_CHECKPOINTER])

    print("Final loss:", model.evaluate(preprocessed_player_boards, player_y, verbose=0))


if os.path.exists(MODEL_CHECKPOINTER.filepath):
    print("Using checkpoint model.")
    model = keras.models.load_model(MODEL_CHECKPOINTER.filepath)
else:
    model = create_model()

model.compile(optimizer='rmsprop', loss='mean_squared_error')

for i in tqdm(range(8)):
    training_iteration(model, 32)
