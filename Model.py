import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras import layers
import matplotlib.pyplot as plt


class RnnToCtc(layers.Layer):
    def __init__(self):
        super(RnnToCtc, self).__init__()
        # self.units = units
        self.kernel = tf.Variable(tf.random.truncated_normal([1, 1, 512, 80], stddev=0.1))

    # def build(self, input_shape):
    #     # stupid shit wtf is this
    #     self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer="random_normal", trainable=True)
    #     self.b = self.add_weight(shape=(self.units,), initializer="random_normal", trainable=True)

    def call(self, inputs, **kwargs):
        return tf.squeeze(
            tf.nn.atrous_conv2d(
                value=inputs,
                filters=self.kernel,
                rate=1, padding='SAME'),
            axis=[2])

    def compute_output_shape(self, input_shape):
        return None, 32, 80


class NeuralNetwork:

    def __init__(self):
        self.input_shape = (128, 32, 3)
        tf.random.normal(self.input_shape)
        self.model = Sequential(
            [
                layers.Conv2D(32, 5, activation='relu', padding='SAME', input_shape=self.input_shape, name="layer1"),
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
                RnnToCtc()
            ]
        )
        self.model.summary()

    def compile(self):
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

    def train(self, train_images, train_labels, test_images, test_labels):
        # compile the model
        self.compile()

        # train the model
        history = self.model.fit(
            train_images,
            train_labels,
            epochs=10,
            validation_data=(test_images, test_labels)
        )

        # show a graphic to see accuracy
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.show()

    def predict(self, image):
        prediction = self.model.predict(image)
        return prediction
