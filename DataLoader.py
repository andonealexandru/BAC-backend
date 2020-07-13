import cv2
import numpy as np
from Alphabet import text_to_label

path_to_file = 'D:/Handwriting DB/ascii/words.txt'  # path catre words.txt
path_to_folder = 'D:/Handwriting DB/words/'  # path catre folderul cu cuvinte
num_images = 100  # pe cate imagini sa se ia din words (pe cate sa antrenam)


def get_x_y():
    f = open(path_to_file)
    count = 0
    x = []  # imaginile
    y = []  # in y sunt labelurile
    x_new = []
    chars = set()
    im_path = []
    for line in f:
        if count > num_images:
            break
        if not line or line[0] == '#':
            continue
        try:
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


def create_input_label_length_and_labels(y):
    y2 = []
    input_lengths = np.ones((num_images, 1)) * 32
    label_lengths = np.zeros((num_images, 1))
    for i in range(num_images):
        val = text_to_label(y[i])
        if i == 5:
            print(val)
        y2.append(val)
        label_lengths[i] = len(y[i])
        input_lengths[i] = 32
    y2 = np.asarray(y2)
    return input_lengths, label_lengths, y2


def get_data():
    x, x_new, y = get_x_y()
    input_lengths, label_lengths, y2 = create_input_label_length_and_labels(y)

    x = np.asarray(x_new[:num_images])  # pastrez doar de cate am nevoie
    x = x[:, :, :, np.newaxis]  # Bx32x128 -> Bx32x128x1
    x = np.transpose(x, (0, 2, 1, 3))  # Bx32x128x1 -> Bx128x32x1

    # normalize images -> toate val intre 0 si 1
    x2 = np.array(x[:num_images]) / 255

    y2 = np.asarray(y2)
    y2 = np.array(y2[:num_images])
    y2 = np.array(y2)

    input_lengths = input_lengths[:num_images]
    label_lengths = label_lengths[:num_images]

    return x2, y2, input_lengths, label_lengths


def extract_img(img):
    target = np.ones((32, 128)) * 255
    new_x = 32 / img.shape[0]
    new_y = 128 / img.shape[1]
    min_xy = min(new_x, new_y)
    new_x = int(img.shape[0] * min_xy)
    new_y = int(img.shape[1] * min_xy)
    img2 = cv2.resize(img, (new_y, new_x))
    target[:new_x, :new_y] = img2[:, :, 0]
    target[new_x:, new_y:] = 255
    return target
