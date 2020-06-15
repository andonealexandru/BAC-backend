class data:
    def __init__(self, path_to_img, lbl):
        self.path_img = path_to_img
        self.label = lbl


def get_lines():
    path = "D:/handWriting DB/words.txt"
    trainingData = []
    with open (path, "r") as myfile:
        txt_data=myfile.readlines()
    for line in txt_data:
        if line[0] != '#':
            words = line.split()
            line_label = words[8]  # words/a01/a01-000u/a01-00u-00-00.png
            aux = words[0].split('-')
            #print(aux)
            path_to_img = "D:/handWriting DB/words/" + aux[0] + "/" + aux[0] + "-" + aux[1] + "/" + words[0] + ".png"
            #print(path_to_img)
            trainingData.append(data(path_to_img, line_label))
    print(trainingData[0].path_img, trainingData[0].label, sep=' ')


get_lines()