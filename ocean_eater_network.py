from collections import deque

from keras import Sequential
from keras.layers import LSTM, Dense, Conv2D, Reshape

import training


def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(Conv2D(32, (2, 2), activation='relu'))

    model.add(Reshape((5*5*32,)))
    model.add(Dense(64))
    model.add(Dense(8))
    model.add(Dense(1, activation='tanh'))

    return model


def preprocess_decision_trees(tree_deque):
    return training.one_hot_batch(tree_deque)
