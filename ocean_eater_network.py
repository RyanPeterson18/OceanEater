import keras
from keras import Sequential
from keras.layers import LSTM, Dense, Conv2D


def create_model():
    model = Sequential()
    model.add(Conv2D(32))
    model.add(Conv2D(32))
    model.add(LSTM(64))
    model.add(LSTM(32))
    model.add(Dense(8))
    model.add(Dense(1, activation='tanh'))

    return model
