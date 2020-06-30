from Model2 import NeuralNetwork
import DataLoader
from PIL import Image

data = DataLoader.feed_NN()  # x, y, label_length, input_length

NN = NeuralNetwork(50)
print(len(data[0]))
NN.train(data[0][:44], data[1][:44], data[2][:44], data[3][:44], 0, 0)
# img = Image.open('pixil-frame-0.png')
# print(img.shape)
# NN.predict(img)


""" todo: 1. labelurile sa aiba size 32
          2. data impartita in batchuri de cate 32
          3. preprocesate imaginile ai sa fie alb negru si doar noi sa ii dam expand
          4. avem grija la oberfitting/underfitting
          5. Vedem daca avem nevoie de time distributed 
          6. Drop-out?
"""