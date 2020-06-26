from PIL import Image
import numpy


class Data:
    def __init__(self, path_to_img, lbl):
        self.path_to_image = path_to_img
        self.label = lbl
        self.label_length = len(lbl)

training_data = []
X = []
y = []
label_length = []

def text_to_label(text):
    alphabet = ' {}[]!”#&’()*+,-./|\\0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ret = []
    for char in text:
        ret.append(alphabet.find(char))
    return ret

def init_input_length():
    inp = numpy.ones(len(label_length), dtype=int)*32
    return inp

def add_list(root_path, data, line):
    words = line.split()
    line_label = words[8]  # words/a01/a01-000u/a01-00u-00-00.png
    aux = words[0].split('-')
    path_to_img = 'D:/Handwriting DB/words/' + aux[0] + \
                  "/" + aux[0] + "-" + aux[1] + "/" + words[0] + ".png"

    data.append(Data(path_to_img, line_label))




def init_train_dataset(path_to_data_root):


    path_to_trainset = 'D:/Handwriting DB/New folder/short_trainset.txt'
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
            if index_train > 2:
                return
            prefix_str = line[:(len(txt_train_file[index_train]) - 1)]
            if prefix_str == txt_train_file[index_train][:len(prefix_str)]:
                found_at_least_once = True
                add_list(path_to_data_root, training_data, line)
    print(index_train)

def feed_NN():
    """returneaza imagini, label, label_length, input_lengh"""
    for data in training_data:
        image = resize_img(data.path_to_image, "images/save_me_here.png", False)
        print("Processing image " + data.path_to_image)
        img_as_array = numpy.asarray(image)
        X.append(img_as_array)
        y.append(text_to_label(data.label))
        label_length.append(data.label_length)

    return X, y, label_length, init_input_length()
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

init_train_dataset('D:/Mirela/Desktop/Projects_dpit_technovation_etc/DPIT-2020/training_data/')
feed_NN()