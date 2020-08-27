from Model import NeuralNetwork
from mainWordSegmentation import getImages, send_words_to_nn
from DataLoader import get_data
from DataLoader import prepare_image
import numpy as np
import matplotlib.pyplot as plt
import cv2


#images, labels, input_lengths, label_Lengths = get_data()
#images = np.asarray(images)
#labels = np.asarray(labels)
#input_lengths = np.asarray(input_lengths)
#label_Lengths = np.asarray(label_Lengths)

# print(images.shape)
# print(labels.shape)
# print(input_lengths.shape)
# print(label_Lengths.shape)

image = cv2.imread("imageToSave.png", 1)
print(send_words_to_nn(image))
