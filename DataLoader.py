from PIL import Image
import numpy


class Data:
    def __init__(self, path_to_img, lbl):
        self.path_to_image = path_to_img
        self.label = lbl
        self.label_length = len(lbl)


training_data = []
Xsir = []
labels = []
label_length = []
input_length = []

validation_data = []
validation_img = []
validation_label = []
val_label_length = []
val_input_length = []

def text_to_label(text):
    alphabet = ' {}[]!"#&’()*+,-./|\\0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ret = []
    for idx in range(0, 32):
        if idx < len(text):
            if text[idx] == '\'':
                ret.append(9)
                continue
            if alphabet.find(text[idx]) == -1:
                print('could not recognize:' + text[idx])
                ret.append(0)
            else:
                ret.append(alphabet.find(text[idx]))
        else:
            ret.append(len(alphabet))  # blank character
    return ret


def add_list(root_path, data, line):
    words = line.split()
    line_label = words[8]  # words/a01/a01-000u/a01-00u-00-00.png
    aux = words[0].split('-')
    path_to_img = 'D:/Handwriting DB/words/' + aux[0] + \
                  "/" + aux[0] + "-" + aux[1] + "/" + words[0] + ".png"

    data.append(Data(path_to_img, line_label))


def init_validationset(path_to_data_root):
    path_to_val = 'D:/Handwriting DB/New folder/validationset.txt'
    with open(path_to_val, "r") as train_file:
        txt_validation_file = train_file.readlines()
    index_train = 0
    path_to_labels = 'D:/Handwriting DB/words/words.txt'

    with open(path_to_labels, "r") as labels_file:
        txt_labels_file = labels_file.readlines()

    found_at_least_once = False
    txt_validation_file.sort()
    txt_labels_file.sort()
    for line in txt_labels_file:
        prefix_str = line[:(len(txt_validation_file[index_train]) - 1)]

        if prefix_str == txt_validation_file[index_train][:len(prefix_str)]:
            found_at_least_once = True
            add_list(path_to_data_root, validation_data, line)
        elif found_at_least_once:
            index_train += 1
            found_at_least_once = False
            print(str(len(txt_validation_file)) + ' ' + str(index_train))
            if index_train >= len(txt_validation_file):
                return

            prefix_str = line[:(len(txt_validation_file[index_train]) - 1)]

            if prefix_str == txt_validation_file[index_train][:len(prefix_str)]:
                found_at_least_once = True
                add_list(path_to_data_root, validation_data, line)


def init_train_dataset(path_to_data_root):

    path_to_trainset = 'D:/Handwriting DB/New folder/trainset.txt'
    with open(path_to_trainset, "r") as train_file:
        txt_train_file = train_file.readlines()
    index_train = 0
    path_to_labels = 'D:/Handwriting DB/words/words.txt'

    with open(path_to_labels, "r") as labels_file:
        txt_labels_file = labels_file.readlines()

    found_at_least_once = False
    txt_train_file.sort()
    txt_labels_file.sort()
    for line in txt_labels_file:
        prefix_str = line[:(len(txt_train_file[index_train])-1)]

        if prefix_str == txt_train_file[index_train][:len(prefix_str)]:
            found_at_least_once = True
            add_list(path_to_data_root, training_data, line)
        elif found_at_least_once:
            index_train += 1
            found_at_least_once = False
            print(str(len(txt_train_file)) + ' ' + str(index_train))
            if index_train >= len(txt_train_file):
                return

            prefix_str = line[:(len(txt_train_file[index_train]) - 1)]

            if prefix_str == txt_train_file[index_train][:len(prefix_str)]:
                found_at_least_once = True
                add_list(path_to_data_root, training_data, line)


def feed_NN():
    init_train_dataset('D:/Mirela/Desktop/Projects_dpit_technovation_etc/DPIT-2020/training_data/')
    # init_validationset('D:/Mirela/Desktop/Projects_dpit_technovation_etc/DPIT-2020/training_data/')
    """returneaza imagini, label, label_length, input_lengh"""
    for data in training_data:
        try:
            image = resize_img(data.path_to_image, "images/save_me_here.png", False)
            print("Processing image " + data.path_to_image + ' size ' + str(image.size))
            img_as_array = numpy.transpose(numpy.asarray(image), (1, 0, 2))
        except:
            print('error')
            continue
        labels.append(text_to_label(data.label))
        label_length.append(data.label_length)
        input_length.append(32)
        Xsir.append(img_as_array)

    labels_as_numpy = numpy.asarray(labels)
    print(labels_as_numpy.shape)

    # for data in validation_data:
    #     try:
    #         image = resize_img(data.path_to_image, "images/save_me_here.png", False)
    #         print("Processing image " + data.path_to_image + ' size ' + str(image.size))
    #         img_as_array = numpy.transpose(numpy.asarray(image), (1, 0, 2))
    #     except:
    #         print('error')
    #         continue
    #     validation_label.append(text_to_label(data.label))
    #     val_label_length.append(data.label_length)
    #     val_input_length.append(32)
    #     validation_img.append(img_as_array)
    #
    # val_labels_numpy = numpy.asarray(validation_label)
    # , validation_img, val_labels_numpy, val_label_length, val_input_length

    return Xsir, labels_as_numpy, label_length, input_length
    # model.fit(X, y, batch_size = 64, epochs = 2)


def get_lines(input_path):
    path = input_path + "ascii/few_words.txt"
    training_data = []

    with open(path, "r") as my_file:
        txt_data = my_file.readlines()

    for line in txt_data:
        if line[0] != '#':
            words = line.split()
            line_label = words[8]  # words/a01/a01-000u/a01-00u-00-00.png
            aux = words[0].split('-')
            path_to_img = input_path + "words/" + aux[0] +\
                          "/" + aux[0] + "-" + aux[1] + "/" + words[0] + ".png"

            img = Image.open(path_to_img)
            training_data.append(Data(path_to_img, line_label, img))

    print(training_data[0].path_img, training_data[0].label, sep=' ')


def recolor(image):
    width = image.size[0]
    height = image.size[1]
    for x in range(width):
        for y in range(height):
            color = (255, 255, 255)
            image.putpixel((x, y), color)


def resize_img(path, output_path, save):
    img = Image.open(path)  # image extension *.png,*.jpg
    wanted_width = 128
    wanted_height = 32
    old_width = img.size[0]
    old_height = img.size[1]
    new_width = 0
    new_height = 0
    if old_width/wanted_width > old_height/wanted_height:
        ratio = old_width/wanted_width
        new_width = wanted_width
        new_height = int(old_height/ratio)
    else:
        ratio = old_height/wanted_height
        new_height = wanted_height
        new_width = int(old_width/ratio)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    new_image = Image.new("RGB", (wanted_width, wanted_height))
    recolor(new_image)
    new_image.paste(img, (0, 0))

    if save:
        new_image.save(output_path)
    return new_image