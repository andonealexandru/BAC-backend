import numpy as np
import tensorflow as tf
from keras.models import Sequential
from tensorflow.keras import layers
from tensorflow import keras
import matplotlib.pyplot as plt


class NeuralNetwork:

    def __init__(self, nmb_characters, max_text_len):
        self.inputs = keras.Input(shape=(128, 32, 3))
        self.setup_model(nmb_characters, max_text_len)

    def setup_model(self, nmb_characters, max_text_len):
            # layers pentru CNN
            conv1 = layers.Conv2D(32, 5, activation='relu', padding='SAME', name="layer1")(self.inputs)
            max1 = layers.MaxPool2D(2, name='layer1pool', padding='VALID')(conv1)
            conv2 = layers.Conv2D(64, 5, activation='relu', padding='SAME', name="layer2")(max1)
            max2 = layers.MaxPool2D(2, name='layer2pool', padding='VALID')(conv2)
            conv3 = layers.Conv2D(128, 3, activation='relu', padding='SAME', name="layer3")(max2)
            max3 = layers.MaxPool2D((1, 2), name='layer3pool', padding='VALID')(conv3)
            conv4 = layers.Conv2D(128, 3, activation='relu', padding='SAME', name="layer4")(max3)
            max4 = layers.MaxPool2D((1, 2), name='layer4pool', padding='VALID')(conv4)
            conv5 = layers.Conv2D(256, 3, activation='relu', padding='SAME', name="layer5")(max4)
            max5 = layers.MaxPool2D((1, 2), name='layer5pool', padding='VALID')(conv5)
            resh = layers.Reshape((32, 256), name='reshape')(max5)

            # RNN
            bid = layers.Bidirectional(layers.LSTM(256, return_sequences=True), name='bidirectLayer')(resh)  # posibil
            # sa avem nevoie de doua layere
            resh2 = layers.Reshape((32, 1, 512), name='resahpeForCtc')(bid)

            kernel = tf.Variable(tf.random.truncated_normal([1, 1, 512, 80], stddev=0.1))
            rnntoCtc = tf.squeeze(tf.nn.atrous_conv2d(value=resh2, filters=kernel, rate=1, padding='SAME'), axis=[2],
                                  name='squeeze_pentru_ctc')

            # din BxTxC in TxBxC - pentru beam search
            ctcin3dtbc = tf.transpose(rnntoCtc, [1, 0, 2])


            # CTC
            y_true = keras.Input(name='truth_labels', shape=(max_text_len,))  # (samples, max_string_length)
            y_pred = rnntoCtc  # am observat ca multa lume foloseste outputul de la inca un layer de activation(softmax)
            # sau time-distributed, nu stiu daca e necesar...
            input_length = keras.Input(name='input_length', shape=(1,))  # lungimea cuvantului din imagine din y_pred
            label_length = keras.Input(name='label_length', shape=(1,))  # lungimea cuvantului din imaginea din y_true

            self.loss_out = layers.Lambda(
                ctc_loss, output_shape=(1,), name='ctc'
            )([y_pred, y_true, label_length, input_length])

            self.model = keras.Model(inputs=[self.inputs, y_true, input_length, label_length], outputs=self.loss_out)
            self.model.summary()

            # self.model = tf.keras.Model(inputs=self.inputs, outputs=rnntoCtc, name='retea')
            # self.model.summary()

    def compile(self):
        self.model.compile(
            optimizer='adam',
            loss={'ctc', lambda y_true, y_pred:y_pred},
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


def ctc_loss(args):
    y_pred, labels, label_length, input_length = args
    return tf.keras.backend.ctc_batch_cost(labels, y_pred, input_length, label_length)
