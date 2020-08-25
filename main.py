from Model import NeuralNetwork
from mainWordSegmentation import getImages, send_words_to_nn
from DataLoader import get_data, get_x_y_math, get_x_y
from DataLoader import prepare_image
import numpy as np
import matplotlib.pyplot as plt
import cv2


x, y, input_lengths1, label_Lengths1, x_mate, y_mate, input_lengths2, label_lengths2 = get_data(evaluate=False, nr_img=1000)
x = np.array(x)
x_mate = np.array(x_mate)
images = np.concatenate((x, x_mate))
labels = np.concatenate((y, y_mate))
input_lengths = np.concatenate((input_lengths1, input_lengths2))
label_Lengths = np.concatenate((label_Lengths1, label_lengths2))

images = np.asarray(images)
labels = np.asarray(labels)
input_lengths = np.asarray(input_lengths)
label_Lengths = np.asarray(label_Lengths)

num = len(images)
places = np.arange(num)
print(num)

np.random.shuffle(places)
images = images[places]
labels = labels[places]
input_lengths = input_lengths[places]
label_Lengths = label_Lengths[places]

nn = NeuralNetwork(create=True, batch_norm=True, dropout=0.5)
nn.train(train_images=images, train_labels=labels,
         label_length=label_Lengths, input_length=input_lengths,
         validation_split=0.15, batch_size=32, epochs=5)
