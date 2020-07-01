
alphabet = ' {}[]!”#&’()*+,-./|\\0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
alp_len = len(alphabet)


# din text in label
def text_to_label(text):
    ret = []
    for char in text:
        ret.append(alphabet.find(char))
    return ret


def labels_to_text(labels):
    res = ''
    for i in range(0, len(labels)):
        if int(labels[i]) < len(alphabet):
            res =res + alphabet[labels[i]]
    return res
