
alphabet = ' {}[]!"#&’()*+,-./|\\0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
alp_len = len(alphabet)


# din text in label
def text_to_label(text):
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


def labels_to_text(labels):
    res = ''
    for i in range(0, len(labels)):
        if int(labels[i]) < len(alphabet):
            res =res + alphabet[labels[i]]
    return res
