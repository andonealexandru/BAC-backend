from Model import NeuralNetwork
from PIL import Image
import numpy as np
import Alphabet as alp
import DataLoader
from  BeamSearch import ctcBeamSearch

NN = NeuralNetwork(50)


# NN = NeuralNetwork(50)
# print(len(data[0]))
# print('minimum pixel:' + str(np.amin(data[0])))
# print('minimum label:' + str(np.amin(data[1])))
# print('minimum label_length:' + str(np.amin(data[2])))
# print('minimum input_length:' + str(np.amin(data[3])))
# if np.amin(data[1]) < 0:
#     print('negative values found')
# else:
#     # training
#     NN.train(data[0], data[1], data[2], data[3], 0, 0, 32, 3)
#     mat = NN.return_text(data[0][1]) # expected: MOVE
#     print('text gasit:' + mat)
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