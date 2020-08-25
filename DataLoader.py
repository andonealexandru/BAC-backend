import cv2
import os
import numpy as np
from Alphabet import text_to_label

path_to_file = 'D:/Handwriting DB/ascii/words.txt'  # path catre words.txt
path_to_folder = 'D:/Handwriting DB/words/'  # path catre folderul cu cuvinte
num_images = 1000  # pe cate imagini sa se ia din words (pe cate sa antrenam)

path_to_file_math = 'D:/dpit2020/jungomi-datasets-crohme-png-1/groundtruth_train.tsv'
path_to_folder_math = 'D:/dpit2020/jungomi-datasets-crohme-png-1/train/'


def get_x_y_math():
    print('hi')
    f = open(path_to_file_math)
    count = 0
    x = []  # imaginile
    y = []  # in y sunt labelurile
    x_new = []
    im_path = []
    for i, line in enumerate(f):
        try:
            # if i>27:
            #     continue
            lineSplit = line.strip().split('\t')
            img_path = path_to_folder_math+lineSplit[0]+'.png'
            img = cv2.imread(img_path)
            # convert image:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            cv2.imwrite('test_crop_init.png', img)

            img = np.asarray(img)
            # trim image to only contain the text:
            non_empty_columns = np.where(img.min(axis=0) <255)[0]
            non_empty_rows = np.where(img.min(axis=1) <255)[0]
            cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

            image_data_new = img[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1]

            folder_img = lineSplit[0].strip().split('/')
            if folder_img[0] == 'MathBrush':
                img = img
            else:
                ret, img = cv2.threshold(image_data_new, 120, 255, cv2.THRESH_BINARY)
            cv2.imwrite('test_crop.png', img)
            img2 = extract_img(img)
            if folder_img[0] == 'MathBrush':
                kernel = np.ones((2, 2))
                img = cv2.erode(image_data_new, kernel, iterations=1)

                img = extract_img(img)
                kernel = np.ones((2, 2))
                img = cv2.erode(img, kernel, iterations=1)
                ret, img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
            else:
                img = cv2.adaptiveThreshold(img2.astype('uint8'), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)
                kernel = np.ones((2, 2))
                img = cv2.erode(img, kernel, iterations=1)
            # img = cv2.erode(th3, (2, 2), iterations=1)
            # print(folder_img[0] +' '+ folder_img[1])
            cv2.imwrite('umm.png', img)
            if not os.path.exists('data_out_mate/%s' % folder_img[0]):
                os.mkdir('data_out_mate/%s' % folder_img[0])
            cv2.imwrite('data_out_mate/%s/%s.png'%(folder_img[0], folder_img[1]), img.astype('uint8'))

            x.append(img)
            text = lineSplit[1]
            if folder_img[0] != 'Hamex':
                text = text.replace(' ', '')
            if folder_img[0] == 'MathBrush':
                text = text.replace('{', '')
                text = text.replace('}', '')
                text = text.replace(' ', '')
            y.append(text)
            # print(text)


            if i%100 == 0:
                print(i)
        except Exception as e:
            print(e)
    return x, y

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
    input_lengths = np.ones((num_images, 1)) * 64
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
        input_lengths[i] = 64
    y2 = np.asarray(y2)
    return input_lengths, label_lengths, y2


def get_data(evaluate, nr_img):
    x, x_new, y = get_x_y(evaluate, nr_img)
    x_mate, y_mate = get_x_y_math()
    input_lengths, label_lengths, y2 = create_input_label_length_and_labels(y, evaluate, nr_img)
    input_lengths2, label_lengths2, y22 = create_input_label_length_and_labels(y_mate, evaluate, nr_img)

    maxim = num_images
    if evaluate:
        maxim = nr_img
    x_mate = np.asarray(x_mate)
    x_mate = x_mate[:, :, :, np.newaxis]
    x_mate = np.transpose(x_mate, (0, 2, 1, 3))
    x_mate = np.array(x_mate)/255

    y_mate = np.asarray(y22)

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

    return x2, y2, input_lengths, label_lengths, x_mate, y_mate, input_lengths2, label_lengths2


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