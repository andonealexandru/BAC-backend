import cv2
import os
import numpy as np
from Alphabet import text_to_label

path_to_file = '/home/andone/Documents/Programming/python/database for train/ascii/words.txt'  # path catre words.txt
path_to_folder = '/home/andone/Documents/Programming/python/database for train/words/'  # path catre folderul cu cuvinte
num_images = 115000  # pe cate imagini sa se ia din words (pe cate sa antrenam)


def get_x_y(evaluate, nr_img):
    f = open(path_to_file)
    count = 0
    x = []  # imaginile
    y = []  # in y sunt labelurile
    x_new = []
    chars = set()
    im_path = []
    for line in f:
        if count > num_images and not evaluate:
            break
        if count > num_images + nr_img:
            break
        if not line or line[0] == '#':
            continue
        try:
            if evaluate and count < num_images:
                count += 1
                continue

            lineSplit = line.strip().split(' ')
            fileNameSplit = lineSplit[0].split('-')
            img_path = path_to_folder + fileNameSplit[0] + '/' + fileNameSplit[
                0] + '-' + \
                       fileNameSplit[1] + '/' + lineSplit[0] + '.png'
            img_word = lineSplit[-1]
            img = cv2.imread(img_path)
            img2 = extract_img(img)
            x_new.append(img2)
            x.append(img)
            y.append(img_word)
            im_path.append(img_path)
            count += 1
            if count % 10 == 0:
                print(count)
        except Exception as e:
            print(e)
    return x, x_new, y


def create_input_label_length_and_labels(y, evaluate, nr_img):
    y2 = []
    input_lengths = np.ones((num_images, 1)) * 32
    label_lengths = np.zeros((num_images, 1))

    maxim = num_images
    if evaluate:
        maxim = nr_img

    for i in range(maxim):
        val = text_to_label(y[i])
        if i == 5:
            print(val)
        y2.append(val)
        label_lengths[i] = len(y[i])
        input_lengths[i] = 32
    y2 = np.asarray(y2)
    return input_lengths, label_lengths, y2


def get_data(evaluate, nr_img):
    x, x_new, y = get_x_y(evaluate, nr_img)
    input_lengths, label_lengths, y2 = create_input_label_length_and_labels(y, evaluate, nr_img)

    maxim = num_images
    if evaluate:
        maxim = nr_img

    x = np.asarray(x_new[:maxim])  # pastrez doar de cate am nevoie
    x = x[:, :, :, np.newaxis]  # Bx32x128 -> Bx32x128x1
    x = np.transpose(x, (0, 2, 1, 3))  # Bx32x128x1 -> Bx128x32x1

    # normalize images -> toate val intre 0 si 1
    x2 = np.array(x[:maxim]) / 255

    y2 = np.asarray(y2)
    y2 = np.array(y2[:maxim])
    y2 = np.array(y2)

    input_lengths = input_lengths[:maxim]
    label_lengths = label_lengths[:maxim]

    return x2, y2, input_lengths, label_lengths


def extract_img(img):
    target = np.ones((32, 128)) * 255
    new_x = 32 / img.shape[0]
    new_y = 128 / img.shape[1]
    min_xy = min(new_x, new_y)
    new_x = int(img.shape[0] * min_xy)
    new_y = int(img.shape[1] * min_xy)
    img2 = cv2.resize(img, (new_y, new_x))

    if len(img2.shape) == 3:
        target[:new_x, :new_y] = img2[:, :, 0]
    else:
        target[:new_x, :new_y] = img2[:, :]

    target[new_x:, new_y:] = 255
    return target


def prepare_image(path):
    data = cv2.imread(path)
    data = cv2.cvtColor(data, cv2.COLOR_RGB2GRAY)
    img = extract_img(data)

    img = np.asarray(img) / 255

    if img.shape[0] == 32:
        img = np.transpose(img, (1, 0))

    if len(img.shape) != 3:
        img = np.expand_dims(img, axis=2)

    return img


def prepare_image_with_img_arg(image):
    if len(image.shape) == 3:
        data = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        data = image
    img = extract_img(data)

    img = np.asarray(img) / 255

    if img.shape[0] == 32:
        img = np.transpose(img, (1, 0))

    if len(img.shape) != 3:
        img = np.expand_dims(img, axis=2)

    return img