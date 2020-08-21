from Model import NeuralNetwork
from mainWordSegmentation import getImages, send_words_to_nn
from DataLoader import get_data
from DataLoader import prepare_image
import numpy as np
import matplotlib.pyplot as plt
import cv2


images, labels, input_lengths, label_Lengths = get_data(evaluate=False, nr_img=1000)
images = np.asarray(images)
labels = np.asarray(labels)
input_lengths = np.asarray(input_lengths)
label_Lengths = np.asarray(label_Lengths)

# print(images.shape)
# print(labels.shape)
# print(input_lengths.shape)
# print(label_Lengths.shape)

nn = NeuralNetwork(create=True, batch_norm=True, dropout=0.5)
# nn.evaluate_model(images, labels, input_lengths, label_Lengths)

nn.train(train_images=images, train_labels=labels,
         validation_split=0.15,
         input_length=input_lengths, label_length=label_Lengths,
         batch_size=32, epochs=5)

print(send_words_to_nn())
