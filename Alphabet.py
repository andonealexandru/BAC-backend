
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
    for l in labels:
        res += alphabet[l]
    return res
