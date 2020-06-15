import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import LSTM
from keras.layers import MaxPool2D


class Model:

    def __init__(self):
        model = Sequential()
        model.add(Conv2D(32, 5, activation='relu', padding='SAME', input_shape=(128, 32)))
        model.add(MaxPool2D(2))
        model.add(Conv2D(64, 5, activation='relu', padding='SAME'))
        model.add(MaxPool2D(2))
        model.add(Conv2D(128, 3, activation='relu', padding='SAME'))
        model.add(MaxPool2D(2))
        model.add(Conv2D(128, 3, activation='relu', padding='SAME'))
        model.add(MaxPool2D(2))
        model.add(Conv2D(256, 3, activation='relu', padding='SAME'))
        model.add(MaxPool2D(2))

        model.summary()
