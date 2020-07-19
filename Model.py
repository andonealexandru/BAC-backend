import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras import layers
from tensorflow import keras
from Alphabet import alp_len, alphabet
from BeamSearch import ctcBeamSearch
import random
from DataLoader import extract_img


class NeuralNetwork:

    def __init__(self):
        self.setup_model()

    @staticmethod
    def setup_model():
        inputs = keras.Input(shape=(128, 32, 1), name='input', dtype='float32')

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
        dense = layers.TimeDistributed(layers.Dense(alp_len + 1))(bid)
        y_pred = layers.TimeDistributed(layers.Activation('softmax', name='softmax'))(dense)

        # CTC
        y_true = keras.Input(name='truth_labels', shape=[32])  # (samples, max_string_length)
        input_length = keras.Input(name='input_length', shape=[1])  # lungimea cuvantului din imagine din y_pred
        label_length = keras.Input(name='label_length', shape=[1])  # lungimea cuvantului din imaginea din y_true
        loss_out = layers.Lambda(
            ctc_loss, output_shape=(1,), name='ctc'
        )([y_pred, y_true, label_length, input_length])

        model = keras.Model(inputs=[inputs, y_true, input_length, label_length], outputs=loss_out)
        model.summary()

        save_model(model)

    @staticmethod
    def train(train_images, train_labels, label_length, input_length, test_images, test_labels, batch_size, epochs):
        model = retrieve_model()
        print('Compiling')
        # keras.losses.custom_loss = {'ctc': lambda y_true, y_pred: y_pred}
        model.compile(
            optimizer=keras.optimizers.Adam(),
            loss={'ctc': ctc_dummy_loss}
        )
        print('Done compiling')

        dataset_to_plot = []
        for i in range(epochs):
            samp = random.sample(range(train_images.shape[0]), batch_size)
            x3 = [train_images[i] for i in samp]
            x3 = np.array(x3)
            y3 = [train_labels[i] for i in samp]
            y3 = np.array(y3)
            input_lengths2 = [input_length[i] for i in samp]
            label_lengths2 = [label_length[i] for i in samp]

            input_lengths2 = np.array(input_lengths2)
            label_lengths2 = np.array(label_lengths2)

            inputs = {
                'input': x3,
                'truth_labels': y3,
                'input_length': input_lengths2,
                'label_length': label_lengths2
            }
            outputs = {'ctc': np.zeros([batch_size])}
            if i % 100 == 0:
                print(i)
                history1 = model.fit(inputs, outputs, batch_size=32, epochs=1, verbose=2)
                dataset_to_plot.append(history1.history['loss'][0])
            else:
                history2 = model.fit(inputs, outputs, batch_size=32, epochs=1, verbose=0)
                dataset_to_plot.append(history2.history['loss'][0])

        print('Done')

        # show a graphic to see loss
        plt.plot(dataset_to_plot)
        plt.title('Training loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid('off')
        plt.show()
        save_model(model)

    @staticmethod
    def predict(image):
        print('predicting')
        model = retrieve_model()
        model2 = keras.Model(model.get_layer('input').input, model.get_layer('time_distributed_1').output)
        model2.summary()
        image = np.expand_dims(image, axis=0)
        prediction = model2.predict(image)
        print(prediction.shape)
        print(np.max(prediction))
        print('done predicting')
        prediction = np.squeeze(prediction, axis=0)
        print(np.max(prediction))
        plt.imshow(prediction)
        plt.imsave('test.jpg', prediction)
        return prediction

    def return_text_from_right_sized_image(self, image):  # pentru imagini care au deja 128x32x1
        mat = self.predict(image)
        return ctcBeamSearch(mat, alphabet, None)

    def return_text_from_random_image(self, image):
        image = extract_img(image)
        image = np.transpose(image, (1, 0))
        print(image.shape)  # ???
        strin = self.return_text_from_right_sized_image(self, image)
        return strin

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


def ctc_dummy_loss(y_true, y_pred):
    return y_pred


def save_model(model):
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    model.save_weights("model.h5")
    print("Saved model to disk")


def retrieve_model():
    print('retrieving model')

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = keras.models.model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    return loaded_model
