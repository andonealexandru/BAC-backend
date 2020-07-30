from Model import NeuralNetwork
from mainWordSegmentation import getImages
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


NN = NeuralNetwork(create=False)

imgs = getImages()

textvb = ''
textws = ''

for i in range(len(imgs)):
    print("for %d" %i)
    img = prepare_image('out/test_cod.jpeg/%d.png'%i)
    textBeam, textWBeam = NN.return_text(img)
    textvb = textvb + ' ' + textBeam
    textws = textws + ' ' + textWBeam

print(textvb)
print(textws)

# img = prepare_image('./hello.png')

# print(img.shape)
# print('Training')
# NN.train(images, labels, label_Lengths, input_lengths, 0, 0, 32, 5)
#print(NN.return_text(images[18]))
# cv2.imshow("imagine", images[55])

# plt.imsave("test55.jpg", images[55])
