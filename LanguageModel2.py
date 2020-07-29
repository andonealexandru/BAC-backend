from __future__ import division
import codecs


class LanguageModel2:
    """Language Model class for beam search"""
    def __init__(self, fn, classes):
        """fn = fisierul cu cuvinte
        classes = alfabetul
        """
        self.initCharBigrams(fn, classes)

    def initCharBigrams(self, fn, classes):
        self.bigram = {c: {d: 0 for d in classes} for c in classes}
        # parcurgerea textului
        txt = codecs.open(fn, 'r', 'utf8').read() # textul
        for i in range(len(txt)-1):
            first = txt[i]
            second = txt[i+1]
            if first not in self.bigram or second not in self.bigram[first]:
                continue

            self.bigram[first][second] += 1

    def getCharBigram(self, first, second):
        """probability of seeing character 'first' next to 'second' """
        first = first if first else ' '
        second = second if second else ' '
        numBigrams = sum(self.bigram[first].values)
        if numBigrams == 0:
            return 0
        return self.bigram[first][second]/numBigrams  # pentru a ne da float division sus


