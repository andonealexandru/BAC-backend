import numpy as np
import tensorflow as tf
import keras
from keras import layers
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras import layers
from tensorflow import keras
import Alphabet as alp
from BeamSearch import ctcBeamSearch
from math import log

class NeuralNetwork:

    def __init__(self, max_text_len):
        self.setup_model(max_text_len)


    @staticmethod
    def setup_model(max_text_len):
        inputs = keras.Input(shape=(128, 32, 3), name='input')

        # layers pentru CNN
        conv1 = layers.Conv2D(32, 5, activation='relu', padding='SAME', name="layer1")(inputs)
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

        kernel = tf.Variable(tf.random.truncated_normal([1, 1, 512, alp.alp_len + 1], stddev=0.1))
        rnn_to_ctc = tf.squeeze(tf.nn.atrous_conv2d(value=resh2, filters=kernel, rate=1, padding='SAME'), axis=[2],
                                name='squeeze_pentru_ctc')

        # din BxTxC in TxBxC - pentru beam search
        # ctcin3dtbc = tf.transpose(rnn_to_ctc, [1, 0, 2])

        # CTC
        y_true = keras.Input(name='truth_labels', shape=[32])  # (samples, max_string_length)
        y_pred = rnn_to_ctc  # am observat ca multa lume foloseste outputul de la inca un layer de activation(softmax)
        # sau time-distributed, nu stiu daca e necesar...
        input_length = keras.Input(name='input_length', shape=[1])  # lungimea cuvantului din imagine din y_pred
        label_length = keras.Input(name='label_length', shape=[1])  # lungimea cuvantului din imaginea din y_true
        loss_out = layers.Lambda(
            ctc_loss, output_shape=(1,), name='ctc'
        )([y_pred, y_true, label_length, input_length])

        model = keras.Model(inputs=[inputs, y_true, input_length, label_length], outputs=loss_out)
        # model = keras.Model(inputs=inputs, outputs=rnn_to_ctc)
        model.summary()

        save_model(model)

        # self.model = tf.keras.Model(inputs=self.inputs, outputs=rnntoCtc, name='retea')
        # self.model.summary()

    @staticmethod
    def compile():
        model = retrieve_model()

        model.compile(
            optimizer='adam',
            loss={'ctc': lambda y_true, y_pred: y_pred},
            metrics=['accuracy']
        )

        save_model(model)

    def train(self, train_images, train_labels, label_length, input_length, test_images, test_labels):
        # compile the model
        #self.compile()

        model = retrieve_model()
        train_images = np.asarray(train_images)
        train_labels = np.asarray(train_labels)
        label_length = np.asarray(label_length)
        input_length = np.asarray(input_length)
        print(train_images.shape)
        print(train_labels.shape)
        print(label_length.shape)
        print(input_length.shape)

        inputs = {
            'input': train_images,
            'truth_labels': train_labels,
            'input_length': input_length,
            'label_length': label_length

        }
        print('Compiling')
        model.compile(
            optimizer='adam',
            loss={'ctc': lambda y_true, y_pred: y_pred},
            metrics=['accuracy']
        )
        print('Done compiling')

        # train the model
        outputs = {'ctc': np.zeros([32])}
        print('Fitting')
        history = model.fit(
            inputs,
            outputs,
            batch_size=32,
            epochs=10,
            # validation_data=(test_images, test_labels)
        )
        print('Done')
        # saving accuracy in acc.pickle file
        accuracy = history.history['accuracy']
        with open('acc.pickle', 'wb') as f:
            pickle.dump(accuracy, f)
        # saving model in saved_model folder
        save_model(model)

        # show a graphic to see accuracy
        plt.plot(history.history['accuracy'], label='accuracy')
        # plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.show()

    @staticmethod
    def predict(image):
        model = retrieve_model()
        model2 = keras.Model(model.input, model.get_layer('tf_op_layer_squeeze_pentru_ctc').output)
        prediction = model2.predict(image)
        return prediction

    def return_text(self, image):
        mat = self.predict(image)
        return ctcBeamSearch(mat, alp.alphabet, None)

    @staticmethod
    def train_for_user_data(image, label, test_images, test_labels):
        # load old accuracy
        with open('acc.pickle', 'rb') as f:
            old_acc = pickle.load(f)

        # load old model
        model = retrieve_model()
        # train with new info
        history = model.fit(
            image,
            label,
            epochs=2,
            validation_data=(test_images, test_labels)
        )
        # print("[INFO] training model...")
        # model.fit(
        # 	x=[trainAttrX, trainImagesX], y=trainY,
        # 	validation_data=([testAttrX, testImagesX], testY),
        # 	epochs=200, batch_size=8)
        # if accuracy is improved, model trained with new info is saved
        if history.history['accuracy'] > old_acc:
            save_model(model)
            with open('acc.pickle', 'wb') as f:
                pickle.dump(history.history['accuracy'], f)



def ctc_loss(args):
    y_pred = args[0]
    labels = args[1]
    label_length = args[2]
    input_length = args[3]
    return tf.keras.backend.ctc_batch_cost(labels, y_pred, input_length, label_length)


def save_model(model):
    model.save('saved_model', overwrite=True)


def retrieve_model():
    return keras.models.load_model('saved_model', compile=False)
