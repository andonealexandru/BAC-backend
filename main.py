from Model import NeuralNetwork
from PIL import Image

NN = NeuralNetwork(50)
NN.compile()

img = Image.open('pixil-frame-0.png')
print(img.shape)
NN.predict(img)
