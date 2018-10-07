from collections import deque

from keras import Sequential
from keras.layers import LSTM, Dense, Conv2D

import training


def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(LSTM(64))
    model.add(LSTM(32))
    model.add(Dense(8))
    model.add(Dense(1, activation='tanh'))

    return model


def preprocess_decision_trees(tree_deque):
    return training.one_hot_batch(tree_deque)
