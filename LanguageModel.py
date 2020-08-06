from __future__ import division
from __future__ import print_function

import re  # regex

from PrefixTree import Trie


class LanguageModel:
    """unigram/bigram LM, add-k smoothing"""

    def __init__(self, corpus, chars, wordChars, non_word_chars):
        """
        :param corpus: read text from filename
        :param chars: caracterele gasite in dataset
        :param wordChars: caracterele regasite in cuvinte
        """
        # read from file
        self.wordCharPattern = '[' + wordChars + ']'
        self.wordPattern = self.wordCharPattern + '+'
        words = re.findall(self.wordPattern, corpus)  # gaseste cuvintele care respecta regexul [...]+ din corpus
        uniqueWords = list(set(words))  # fara sa se repete
        self.numWords = len(words)
        self.numUniqueWords = len(uniqueWords)
        # asta inca nu stiu ce inseamna:
        self.smoothing = True
        self.addK = 1.0 if self.smoothing else 0.0

        # creare unigrame
        self.unigrams = {}
        for w in words:
            w = w.lower()
            if w not in self.unigrams:
                self.unigrams[w] = 0
            self.unigrams[w] += 1 / self.numWords

        # create unnormalized bigrams
        bigrams = {}
        for i in range(len(words) - 1):
            w1 = words[i].lower()
            w2 = words[i + 1].lower()
            if w1 not in bigrams:
                bigrams[w1] = {}
            if w2 not in bigrams[w1]:
                bigrams[w1][w2] = self.addK  # add-K
            bigrams[w1][w2] += 1

        # normalize bigrams
        for w1 in bigrams.keys():
            # sum up
            probSum = self.numUniqueWords * self.addK  # add-K smoothing
            for w2 in bigrams[w1].keys():
                probSum += bigrams[w1][w2]
            # and divide
            for w2 in bigrams[w1].keys():
                bigrams[w1][w2] /= probSum
        self.bigrams = bigrams

        # cream PrefixTree
        self.tree = Trie()  # arbore prefix gol
        self.tree.add_words(uniqueWords)  # adaug cuvintele


        # liste cu car folosite, nefolosite
        self.allChars = chars
        self.wordChars = wordChars
        self.nonWordChars = non_word_chars

    def get_next_words(self, text):
        """textul trbuie sa fie prefix"""
        return self.tree.get_next_words(text)

    def get_next_chars(self, text):
        nextChars = str().join(self.tree.get_next_chars(text))

        # daca suntem intre doua cuvinte, cuvantul se termina sau non-words caracters
        if(text == '') or (self.is_word(text)):
            nextChars += self.get_non_word_chars()
        return nextChars

    def get_word_chars(self):
        return self.wordChars

    def get_non_word_chars(self):
        return self.nonWordChars

    def get_all_chars(self):
        return self.allChars

    def is_word(self, text):
        return self.tree.is_word(text)

    # todo: modifica pentru caractere
    def get_unigram_probs(self, w):
        """probabilitatea sa vedem cuvantul w"""
        w = w.lower()
        val = self.unigrams.get(w)
        if val is not None:
            return val
        return 0

    def getBigramProb(self, w1, w2):
        "prob of seeing words w1 w2 next to each other."
        w1 = w1.lower()
        w2 = w2.lower()
        val1 = self.bigrams.get(w1)
        if val1 is not None:
            val2 = val1.get(w2)
            if val2 is not None:
                return val2
            return self.addK / (self.get_unigram_probs(w1) * self.numUniqueWords + self.numUniqueWords)
        return 0


# lm = LanguageModel('12 1 13 12 15 234 2526', ' ,.:0123456789', '0123456789')
# prefix = '1'
# print('getNextChars:', lm.get_next_chars(prefix))
# print('getNonWordChars:', lm.get_non_word_chars())
# print('getNextWords:', lm.get_next_words(prefix))
# print('isWord:', lm.is_word(prefix))
# print('getBigramProb:', lm.getBigramProb('12', '15'))
