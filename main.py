import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras import layers


# custom layer for transforming rnn output (32, 1, 512) into (32, 80) for ctc layer
class RnnToCtc(layers.Layer):
    def __init__(self, units=32):
        super(RnnToCtc, self).__init__()
        self.units = units
        self.kernel = tf.Variable(tf.random.truncated_normal([1, 1, 512, 80], stddev=0.1))

    def build(self, input_shape):
        # stupid shit wtf is this
        self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer="random_normal", trainable=True)
        self.b = self.add_weight(shape=(self.units,), initializer="random_normal", trainable=False)

    def call(self, inputs, **kwargs):
        return tf.squeeze(
            tf.nn.atrous_conv2d(
                value=inputs,
                filters=self.kernel,
                rate=1, padding='SAME'),
            axis=[2])

    def compute_output_shape(self, input_shape):
        return None, 32, 80


input_shape = (128, 32, 3)
tf.random.normal(input_shape)
model = Sequential(
    [
        layers.Conv2D(32, 5, activation='relu', padding='SAME', input_shape=input_shape, name="layer1"),
        layers.MaxPool2D(2, name='layer1pool', padding='VALID'),
        layers.Conv2D(64, 5, activation='relu', padding='SAME', name="layer2"),
        layers.MaxPool2D(2, name='layer2pool', padding='VALID'),
        layers.Conv2D(128, 3, activation='relu', padding='SAME', name="layer3"),
        layers.MaxPool2D((1, 2), name='layer3pool', padding='VALID'),
        layers.Conv2D(128, 3, activation='relu', padding='SAME', name="layer4"),
        layers.MaxPool2D((1, 2), name='layer4pool', padding='VALID'),
        layers.Conv2D(256, 3, activation='relu', padding='SAME', name="layer5"),
        layers.MaxPool2D((1, 2), name='layer5pool', padding='VALID'),
        layers.Reshape((32, 256), name='reshape'),
        layers.Bidirectional(layers.LSTM(256, return_sequences=True), name='bidirectLayer'),
        layers.Reshape((32, 1, 512), name='resahpeForCtc'),
        RnnToCtc(),
    ]
)
model.summary()
# trebuie sa aplicam conv2d pe outputul anterior
# atrous-conv2d primeste ca aparametrii:
# value - pe ce aplica
# filters - e [filter_height, filter_width, in_channels, out_channels]
# rate = 1 => conv2d simplu


# kernel = tf.Variable(tf.random.truncated_normal([1, 1, 512, 80], stddev=0.1))
# print(kernel.shape)
# rnnOut3d = tf.squeeze(tf.nn.atrous_conv2d(value=model.layers[12].output, filters=kernel, rate=1, padding='SAME'),
#                       axis=[2])
#
# ctcIn3dTBC = tf.transpose(rnnOut3d, [1, 0, 2])
# print(rnnOut3d.shape)
