from Model import NeuralNetwork
import DataLoader
from PIL import Image

data = DataLoader.feed_NN()

NN = NeuralNetwork(50)
NN.train(data[0], data[1], data[2], data[3], 0, 0)
# img = Image.open('pixil-frame-0.png')
# print(img.shape)
# NN.predict(img)
