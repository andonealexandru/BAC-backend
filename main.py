from Model2 import NeuralNetwork
from DataLoader import get_data
import numpy as np

images, labels, input_lengths, label_Lengths = get_data()
images = np.asarray(images)
labels = np.asarray(labels)
input_lengths = np.asarray(input_lengths)
label_Lengths = np.asarray(label_Lengths)

print(images.shape)
print(labels.shape)
print(input_lengths.shape)
print(label_Lengths.shape)


NN = NeuralNetwork()
print('Training')
NN.train(images, labels, label_Lengths, input_lengths, 0, 0, 32, 5000)

